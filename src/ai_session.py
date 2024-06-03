import logging
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
import os
import dotenv, json
import textwrap
from .extractions import Extractor
from . import extractions

dotenv.load_dotenv()
logger = logging.getLogger("txt2stix.ai_session")

class AIExtractSession:
    def __init__(self, llm):
        self.conversation = ConversationChain(llm=llm)
    @staticmethod
    def openai(model_name=os.getenv("OPENAI_MODEL", "gpt-4")):
        llm = ChatOpenAI(
            temperature=0,
            model_name=model_name
        )
        return AIExtractSession(llm)

    def query(self, query):
        logger.info(f"AI Chat Query: {repr(query)}")
        resp = self.conversation.invoke({"input":query})['response']
        logger.info(f"AI Chat Response: {repr(resp)}")
        return resp

    def set_document(self, txt, raise_for_status=True):
        self.document = txt
        self.conversation.memory.clear()
        template = textwrap.dedent("""
            Here is a body of text. It starts with [txt2stix-input-start] and ends with [txt2stix-input-end] of this prompt. Does it contain any text? If yes, please reply with one word; "successful". If not, please reply with "unsuccessful".
            [txt2stix-input-start]{user_input}[txt2stix-input-end]
        """)
        status = self.query(template.format(user_input=txt))
        if status.lower() != "successful" and raise_for_status:
            raise Exception("set document failed with status:%s"%status)
        return status

    def get_extractors_str(self, extraction_config):
        extractor:Extractor = None
        extractors = []
        for extractor in extraction_config.extractors.values():
            extractor_str = textwrap.dedent(f"""
            ##### {extractor.name} (extraction_key={extractor.extraction_key})
             - {extractor.prompt_base}
             - {extractor.prompt_conversion}
            """)
            extractors.append(extractor_str.format_map(extraction_config))
        return extractors
        
    def extract_observables(self, extraction_config):
        extractors = self.get_extractors_str(extraction_config)
        template = textwrap.dedent("""
        Using the body of text from a cyber-security report (more specifically in the field of cyber threat intelligence) posted in the previous prompt, I would now like you to extract all the following types of cyber-security related data present in it. Each extraction type starts with "###### extractor name". Included with each extractor name heading is an extraction_key. You'll also find more information to help you fine-tune the data you extract for each extractor type below its respective heading.
        
        {extractors}

        """).format(extractors="\n".join(extractors))


        template += """For each extraction, post your response as a valid JSON document using the following structure;

        {"extractions":{"extraction_0":{"type":"<extraction_key>","value":"<extracted_value>","original_text":"<original_text>","start_index":["start_index_n"]},"extraction_n":{"type":"<extraction_key>","value":"<extracted_value>","original_text":"<original_text>","start_index":["start_index_n"]}}}

        Where:

        * "type": is the extraction_key value shown in the list printed earlier in this prompt
        * "value": is the value extracted from the text
        * "original_text": is the original text the extraction was made from
        * "start_index": a list of the index positions of the first character for each matching extraction. Some documents might capture many extractions where `key` and `value` are the same for many entries. This property allows the user to identify how many extractions happened, and where they are in the document.

        Only one JSON object should exist for each unique value. Please use backslash escape characters when quote characters (`"`) are used to ensure the output conforms to the JSON schema.

        Only include a valid JSON document in your response and no other text. The JSON document should be minified, as shown above.
        """

        return json.loads(self.query(template))

    def set_other_extractions(self, all_extracts):
        inp = dict(extractions={})
        for type, value in all_extracts.items():
            if type != "ai":
                inp["extractions"].update(value["extractions"])
        
        query = textwrap.dedent(f"""
        Consider the JSON object on the next line as extractions from an external processor and remember it for later use. Please reply with one word, either "successful" if you have stored the text or "unsuccessful" if there has been an error with this request.
        
        {json.dumps(inp)}
        """)

        return self.query(query)


    def extract_relationships(self, relationship_types:list[str]):
        relationship_types = ",".join(relationship_types)
        query = textwrap.dedent("""
            Using the original text in the first prompt and the extractions in the earlier conversation, please logically describe the relationships between the extractions in the following JSON format. 

            {"relationships":{"relationship_0":{"source_ref":"<source extraction id>","target_ref":"<target extraction id>","relationship_type":"<valid relationship type>"},"relationship_n":{"source_ref":"<source extraction id>","target_ref":"<target extraction id>","relationship_type":"<valid relationship type>"}}}
            
            Where;

            * source_ref: is the id for the source extraction for the relationship (e.g. extraction_1).
            * target_ref: is the index for the target extraction for the relationship (e.g. extraction_2).
            * relationship_type: is a description of the relationship between target and source.  It should be the best matching description for the relationship from the following values: [%s]

            Only include a valid JSON document in your response and no other text. The JSON document should be minified, as shown above.
        """ % relationship_types)

        return json.loads(self.query(query))

    def get_conversation(self):
        out = ""
        for message in self.conversation.memory.dict()["chat_memory"]["messages"]:
            out += f"\n==================== {message['type'].upper().center(9)} ====================\n"
            out += message['content']
        return out

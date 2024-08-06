import io
import logging

from openai import OpenAI
from openai.types.beta.vector_store import ExpiresAfter
import os
import dotenv, json
import textwrap
from .extractions import Extractor
from . import extractions


from llama_index.llms.openai import OpenAI as ChatOpenAI
from llama_index.core.chat_engine import SimpleChatEngine
from llama_index.core.base.llms.types import ChatMessage, MessageRole
import tiktoken

dotenv.load_dotenv()
logger = logging.getLogger("txt2stix.ai_session")

class BaseAIExtractor:
    document = None
    initialized = False
    def set_document(self, document):
        self.document = document
        self.initialized = True
    def extract_objects(self, extractors, input_text):
        raise NotImplementedError("this method should be implemented in subclass")
    def extract_relationships(self, extractions, input_text):
        raise NotImplementedError("this method should be implemented in subclass")
    def get_conversation(self):
        return "CONVERSATION: NotImplemented"
    
    def calculate_token_count(self, text, model='gpt-4o'):
        enc = tiktoken.encoding_for_model(model)
        return len(enc.encode(text))

class OpenAIAssistantExtractor(BaseAIExtractor):
    extract_instruction = textwrap.dedent(
    """
    Using the file above, you are to extract objects from the body of input (either plaintext or markdown), extractions must be unique!

    ```json
    [
        {
            "type": "<extraction_key>",
            "id": "ai-1",
            "value": "<extracted_value>",
            "original_text": "<original_text>",
            "start_index": ["start_index_1"]
        },
        {
            "type": "<extraction_key>",
            "id": "ai-n",
            "value": "<extracted_value>",
            "original_text": "<original_text>",
            "start_index": ["start_index_n"]
        }
    ]
    ```
    Where:

    * `"id"`    => is the id of the extraction of the format `"ai-%d" %(position in list)`, it should start from 1 (e.g `"ai-1", "ai-2", ..., "ai-n"`)
    * `"type"`  => is the extraction_key value shown in the list printed earlier in this prompt
    * `"value"` => is the value extracted from the text
    * `"original_text"` => is the original text the extraction was made from
    * `"start_index"`   => a list of the index positions of the first character for each matching extraction. Some documents might capture many extractions where `key` and `value` are the same for many entries. This property allows the user to identify how many extractions happened, and where they are in the document.

    Only one JSON object should exist for each unique value.

    Only include a valid JSON document in your response and no other text. The JSON document should be minified!.
        
    """)
    relationship_instruction = textwrap.dedent(
    """
        please logically describe the relationships between the extractions in the following JSON format.

        ```json
        [
            {
                "source_ref": "<source extraction id>",
                "target_ref": "<target extraction id>",
                "relationship_type": "<valid relationship type>"
            },
            {
                "source_ref": "<source extraction id>",
                "target_ref": "<target extraction id>",
                "relationship_type": "<valid relationship type>"
            }
        ]
        ```
        
        Where;

        * `source_ref`: is the id for the source extraction for the relationship (e.g. extraction_1).
        * `target_ref`: is the index for the target extraction for the relationship (e.g. extraction_2).
        * `relationship_type`: is a description of the relationship between target and source.


        important: JSON output must be minified!
        """
    )
    def __init__(self, model="gpt-4-turbo", filename="txt2stix-file.md") -> None:
        self.client = OpenAI(timeout=120)
        self.assistant = self.client.beta.assistants.create(
            model=model,
            name="CTI Extractor",
            instructions=textwrap.dedent("""
            You are a CTI extractor, you are to extract objects from the input file and return JSON reponse! 
            IMPORTANT
            - Extractions must be unique
            - All JSON output must be minified!
            """),
            tools=[{"type": "file_search"}],
        )
        self.filename = filename

    def set_document(self, input_text):
        if self.document:
            return
        self.document = io.BytesIO(input_text.encode("utf-8"))
        self.document.name = self.filename
        
        file_obj = self.client.files.create(file=self.document, purpose="assistants")
        self.files = [dict(file_id=file_obj.id, tools=[{"type": "file_search"}])]
        # vector = self.client.beta.vector_stores.create(expires_after=ExpiresAfter(days=1, anchor='last_active_at'), file_ids=[f['file_id'] for f in self.files])
        message = dict(
            role="assistant",
            content="I will be working with this file, all subsequent messages after this will bve working on this file.",
            attachments=self.files,
        )
        self.thread = self.client.beta.threads.create(messages=[message])
        logging.info("created thread at `https://platform.openai.com/playground/assistants?thread=%s`", self.thread.id)

    def get_output(self, instruction, messages = []):
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
            additional_messages=messages,
            additional_instructions=instruction,
            max_completion_tokens=30_000,
            max_prompt_tokens=30_000,
        )

        if run.status == 'completed': 
            messages = self.client.beta.threads.messages.list(
                thread_id=self.thread.id,
                run_id=run.id
            )
            print( messages)
        else:
            print(run.status)

    def extract_objects(self, extractors):
        extractors_str = textwrap.dedent("""
        use the following extractors
        ```json
        {}
        ```
        
        - response must be minified
        """).format(json.dumps([dict(name=extractor.name, extraction_key=extractor.extraction_key, prompt_base=extractor.prompt_base, prompt_converter=extractor.prompt_conversion) for extractor in extractors], indent=2))
        logging.info(extractors_str)
        return self.get_output(extractors_str, [
                dict(
                    role="assistant",
                    content=self.extract_instruction,
                ),
                dict(
                    role="assistant",
                    content="using these extractors: \n\n- {}".format("\n- ".join(ex.name for ex in extractors)),
                ),
            ]
        )
    
    def extract_relationships(self, extractions, relationship_types=[]):
        inputs = []
        for k, v in extractions.items():
            if k != 'ai':
                inputs.extend(v)
        
        messages = [
            dict(
                role="user",
                content=textwrap.dedent("""
                here are more extractions from an external processor;
                
                ```json
                {}
                ```
                """).format(json.dumps(inputs, indent=2))),
            dict(
                role="assistant",
                content=textwrap.dedent("""
                relationship_type must be one of the following values, please pick the most suitable value that logically decribe the relationship between the extractions.

                - {}
                """).format("\n- ".join(relationship_types))
            )
        ]
        return self.get_output(self.relationship_instruction, messages)
    
    def get_conversation(self):
        return f"============ THREAD_URL = `https://platform.openai.com/playground/assistants?thread={self.thread.id}` ==================="

class GenericAIExtractor(BaseAIExtractor):
    engine = None
    model = None
    def __init__(self, llm):
        self.llm=llm
        self.history = []
        self.old_history = []

    @staticmethod
    def openai(model_name=os.getenv("OPENAI_MODEL", "gpt-3.5")):
        llm = ChatOpenAI(model_name=model_name)
        retval = GenericAIExtractor(llm)
        retval.model = model_name
        return retval
    
    def calculate_token_count(self, text, model=None):
        return super().calculate_token_count(text, model or self.model)

    def query(self, query):
        logger.info(f"AI Chat Query: {repr(query)}")
        resp = self.engine.chat(query)
        logger.info(f"AI Chat Response: {repr(resp)}")
        return resp.response.strip().strip("```").strip("json").strip()

    def set_document(self, txt, raise_for_status=True):
        self.document = txt
        template = textwrap.dedent(
            """
            Here is a body of text. It starts with [txt2stix-input-start] and ends with [txt2stix-input-end] of this prompt. Does it contain any text? If yes, please reply with one word; "successful". If not, please reply with "unsuccessful".
            [txt2stix-input-start]{user_input}[txt2stix-input-end]
            """
        )
        if self.engine:
            self.old_history = self.engine.chat_history

        self.history = [
            ChatMessage(
                role=MessageRole.SYSTEM,
                content="You are a CTI extractor, you reply in minified JSON [array of extractions]. The JSON output should not contain ```, it should be plaintext"
            ),
            ChatMessage(
                role=MessageRole.USER,
                content=template.format(user_input=txt)
            ),
            ChatMessage(
                role=MessageRole.ASSISTANT,
                content="successful"
            )
        ]
        self.engine = SimpleChatEngine.from_defaults(chat_history=self.history, llm=self.llm)

    def get_extractors_str(self, extractors):
        extractor: Extractor = None
        extractors_str = []
        for extractor in extractors:
            extractor_str = textwrap.dedent(
            f"""
            ##### {extractor.name} (extraction_key={extractor.extraction_key})
            - {extractor.prompt_base}
            - {extractor.prompt_conversion}
            """
            )
            extractors_str.append(extractor_str)
        return extractors_str

    def extract_objects(self, extractors):
        extractors = self.get_extractors_str(extractors)
        template = textwrap.dedent(
            """
        Using the body of text from a cyber-security report (more specifically in the field of cyber threat intelligence) posted in the previous prompt, I would now like you to extract all the following types of cyber-security related data present in it. Each extraction type starts with "###### extractor name". Included with each extractor name heading is an extraction_key. You'll also find more information to help you fine-tune the data you extract for each extractor type below its respective heading.
        
        {extractors}

        """
        ).format(extractors="\n".join(extractors))

        template += """For each extraction, post your response as a valid JSON document using the following structure;

        ```json
        [
            {
                "type": "<extraction_key>",
                "id": "ai-1",
                "value": "<extracted_value>",
                "original_text": "<original_text>",
                "start_index": ["start_index_1"]
            },
            {
                "type": "<extraction_key>",
                "id": "ai-n",
                "value": "<extracted_value>",
                "original_text": "<original_text>",
                "start_index": ["start_index_n"]
            }
        ]
        ```
        Where:

        * "id": is the id of the extraction of the format `"ai-%d" %(position in list)`, it should start from 1 (e.g "ai-1", "ai-2", ..., "ai-n")
        * "type": is the extraction_key value shown in the list printed earlier in this prompt
        * "value": is the value extracted from the text
        * "original_text": is the original text the extraction was made from
        * "start_index": a list of the index positions of the first character for each matching extraction. Some documents might capture many extractions where `key` and `value` are the same for many entries. This property allows the user to identify how many extractions happened, and where they are in the document.

        Only one JSON object should exist for each unique value. Please use backslash escape characters when quote characters (`"`) are used to ensure the output conforms to the JSON schema.

        Only include a valid JSON document in your response and no other text. The JSON document should be minified, as shown above.
        """

        return json.loads(self.query(template))

    def set_other_extractions(self, all_extracts):
        inp = []
        for type, value in all_extracts.items():
            inp.extend(value)

        query = textwrap.dedent(
            f"""
        Consider the JSON object on the next line as extractions from an external processor and remember it for later use.
        
        {json.dumps(inp)}
        """
        )

        return self.engine.chat_history.append(ChatMessage(content=query, role=MessageRole.USER))

    def extract_relationships(self, extractions, relationship_types: list[str]):
        relationship_types = ",".join(relationship_types)
        self.set_other_extractions(extractions)
        query = textwrap.dedent(
            """
            Using the original text in the first prompt and the extractions in the earlier conversation, please logically describe the relationships between the extractions in the following JSON format. 

            ```json
                [
                    {
                        "source_ref": "<source extraction id>",
                        "target_ref": "<target extraction id>",
                        "relationship_type": "<valid relationship type>"
                    },
                    {
                        "source_ref": "<source extraction id>",
                        "target_ref": "<target extraction id>",
                        "relationship_type": "<valid relationship type>"
                    }
                ]
            ```
            
            Where;

            * source_ref: is the id for the source extraction for the relationship (e.g. extraction_1).
            * target_ref: is the index for the target extraction for the relationship (e.g. extraction_2).
            * relationship_type: is a description of the relationship between target and source.  It should be the best matching description for the relationship from the following values: [%s]

            Only include a valid JSON document in your response and no other text. The JSON document should be minified, as shown above.
        """
            % relationship_types
        )

        return json.loads(self.query(query))

    def get_conversation(self):
        out = ""
        for message in self.old_history:
            out += f"\n==================== {message.role} ====================\n"
            out += message.content
        if self.old_history:
            out += "\n\n"
            out += "========================================================\n"*4
        for message in self.engine.chat_history:
            out += f"\n==================== {message.role} ====================\n"
            out += message.content
        return out

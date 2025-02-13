
from llama_index.core import PromptTemplate, ChatPromptTemplate
import textwrap
from llama_index.core.base.llms.types import ChatMessage, MessageRole


DEFAULT_SYSTEM_PROMPT = textwrap.dedent(
"""
<persona>

    You are a cyber-security threat intelligence analysis tool responsible for analysing intelligence provided in text files.

    You have a deep understanding of cybersecurity and threat intelligence concepts.

    IMPORTANT: You must always deliver your work as a computer-parsable output in JSON format. All output from you will be parsed with pydantic for further processing.

</persona>
"""
)

DEFAULT_EXTRACTION_TEMPL = PromptTemplate(textwrap.dedent(
    """
    <persona>
        You are a cyber-security threat intelligence analysis tool responsible for analysing intelligence provided in text files.
        You have a deep understanding of cybersecurity and threat intelligence concepts.
        IMPORTANT: You must always deliver your work as a computer-parsable output in JSON format. All output from you will be parsed with pydantic for further processing.
    </persona>
    <requirements>
        Using the report text printed between the `<document>` tags, you should extract the Indicators of Compromise (IoCs) and Tactics, Techniques, and Procedures (TTPs) being described in it.
        The document can contain the same IOC or TTP one or more times. Only create one record for each extraction -- the extractions must be unique!
        Only one JSON object should exist for each unique value.
    </requirements>
    <accuracy>
        Think about your answer first before you respond. The accuracy of your response is very important as this data will be used for operational purposes.
        If you don't know the answer, reply with success: false, do not ever try to make up an answer.
    </accuracy>
    <document>
    {input_file}
    </document>
    <extractors>
    {extractors}
    </extractors>
    <response>
        IMPORTANT: Only include a valid JSON document in your response and no other text. The JSON document should be minified!.
        Response MUST be in JSON format.
        Response MUST start with: {"success":
    </response>
    """
))


DEFAULT_RELATIONSHIP_TEMPL = PromptTemplate(textwrap.dedent(
"""
<persona>
    You are a cyber-security threat intelligence analysis tool responsible for analysing intelligence provided in text files.
    You have a deep understanding of cybersecurity and threat intelligence concepts.
    IMPORTANT: You must always deliver your work as a computer-parsable output in JSON format. All output from you will be parsed with pydantic for further processing.
</persona>
<requirements>
    The tag `<extractions>` contains all the observables and TTPs that were extracted from the document provided in `<document>`
    Please capture the relationships between the extractions and describe them using NLP techniques.
    A relationship MUST have different source_ref and target_ref
    Select an appropriate relationship_type from `<relationship_types>`.
    Only use `related-to` or any other vague `relationship_type` as a last resort. 
    The value of relationship_type MUST be clear, and it SHOULD NOT describe everything as related-to each other unless they are related in context of the `<document>
    IMPORTANT: Only include a valid JSON document in your response and no other text. The JSON document should be minified!.
</requirements>
<accuracy>
    Think about your answer first before you respond. The accuracy of your response is very important as this data will be used for operational purposes.
    If you don't know the answer, reply with success: false, do not ever try to make up an answer.
</accuracy>
<document>
{input_file}
</document>
<extractions>
{extractions}
</extractions>
<relationship_types>
{relationship_types}
</relationship_types>
<response>
    IMPORTANT: Only include a valid JSON document in your response and no other text. The JSON document should be minified!.
    Response MUST be in JSON format.
    Response MUST start with: {"success":
</response>
"""
))

DEFAULT_CONTENT_CHECKER_TEMPL = PromptTemplate("""
<persona>
    You are a cyber security threat intelligence analyst.
    Your job is to review report that describe a cyber security incidents.
    Examples include malware analysis, APT group reports, data breaches, vulnerabilities, or Indicators of Compromise.
    Some of the documents you are given do not help in this 
    I need you to tell me if the text provided is.
</persona>
<requirement>
    Using the MARKDOWN of the report provided in <document>
    IMPORTANT: the output should be structured as valid JSON.
    IMPORTANT: output should not be in markdown, it must be a plain JSON text without any code block
    IMPORTANT: do not include any comment in the output
    IMPORTANT: output must start with a `{` and end with a `}` and must not contain "```"
</requirement>
<document>
{context_str}
</document>
<incident_classification>
    Possible Incident Classifications are
    * Other: the report does not fit into any of the following categories
    * APT Group
    * Vulnerability
    * Data Leak
    * Malware
    * Ransomware
    * Infostealer
    * Threat Actor
    * Campaign
    * Exploit
    * Cyber Crime
    * Indicators of Compromise
    * TTPs
</incident_classification>
""")

ATTACK_FLOW_PROMPT_TEMPL = ChatPromptTemplate([
    ChatMessage.from_str("""You are a cyber security threat intelligence analyst.
Your job is to review report that describe a cyber security incidents.
Examples include malware analysis, APT group reports, data breaches and vulnerabilities.""", MessageRole.SYSTEM),
    ChatMessage.from_str("Hi, What <document> would you like me to process for you? the message below must contain the document and the document only", MessageRole.ASSISTANT),
    ChatMessage.from_str("{document}", MessageRole.USER),
    ChatMessage.from_str("What are the objects that have been extracted (<extractions>) from the document above?", MessageRole.ASSISTANT),
    ChatMessage.from_str("{extractions}", MessageRole.USER),
    ChatMessage.from_str("What are the relationships that have been extracted (<relationships>) between the documents?", MessageRole.USER),
    ChatMessage.from_str("{relationships}", MessageRole.USER),
    ChatMessage.from_str("What should I do with all the data that have been provided?", MessageRole.ASSISTANT),
    ChatMessage.from_str("""Consider all the MITRE ATT&CK Objects extracted from the report and the relationships they have to other objects.

Now I need you to logically define the order of ATT&CK Tactics/Techniques as they are executed in the incident described in the report.

It is possible that the Techniques extracted are not linked to the relevant MITRE ATT&CK Tactic. You should also assign the correct Tactic to a Technique where a Technique belongs to many ATT&CK Tactics in the ATT&CK Matrix if that can correctly be inferred.

You should also provide a short overview about how this technique is described in the report as the name, and a longer version in description.

IMPORTANT: only include the ATT&CK IDs extracted already, do not add any new extractions.

You should deliver a response in JSON as follows

[
{
   "position": "<ORDER OF OBJECTS STARTING AT 0",
   "attack_tactic_id": "<ID>",
   "attack_technique_id": "<ID>",
   "name": "<NAME>",
   "description": "<DESC>"
},
{
   "position": "<ORDER OF OBJECTS STARTING AT 0",
   "attack_tactic_id": "<ID>",
   "attack_technique_id": "<ID>",
   "name": "<NAME>",
   "description": "<DESC>"
}
]""", MessageRole.USER)
])
from pydantic import BaseModel, Field

class Extraction(BaseModel):
    type : str = Field(description="is the extraction_key value shown in the list printed earlier in this prompt")
    id: str =  Field(description='is the id of the extraction of the format `"ai-%d" %(position in list)`, it should start from 1 (e.g `"ai-1", "ai-2", ..., "ai-n"`)')
    value: str  =  Field(description='is the value extracted from the text')
    original_text: str =  Field(description='is the original text the extraction was made from')
    start_index: list[str|int] =  Field(default_factory=list, description='no result expected')


class Relationship(BaseModel):
    source_ref: str = Field(description='is the id for the source extraction for the relationship (e.g. extraction_1).')
    target_ref: str = Field(description='is the index for the target extraction for the relationship (e.g. extraction_2).')
    relationship_type: str = Field(description='is a description of the relationship between target and source.')

class ExtractionList(BaseModel):
    extractions: list[Extraction] = Field(default_factory=list)
    success: bool

class RelationshipList(BaseModel):
    relationships: list[Relationship] = Field(default_factory=list)
    success: bool

    def get(self, key, default=None):
        return getattr(self, key, default)

class DescribesIncident(BaseModel):
    describes_incident: bool = Field(description="does the <document> include malware analysis, APT group reports, data breaches and vulnerabilities?")
    explanation: str = Field(description="Two or three sentence summary of the incidents it describes OR summary of what it describes instead of an incident")
    incident_classification : list[str] = Field(description="All the valid incident classifications that describe this document/report")
    summary: str = Field(description="executive summary of the document containing no more than one paragraphs.")
    threat_score: int = Field(description="a threat score for this report on a scale of `0` to `100`, where `0` indicates no threat and `100` indicates an extremely high threat. Always zero for documents that do not describe an incident.", default=0)
    threat_score_explanation: str = Field(description="explanation of the reasoning behind the assigned threat score", default="")
    language: str = Field(description="the ISO 639-1 two-letter language code (e.g. `en`, `fr`, `de`) of the language the <document> is primarily written in", default="")

class AttackFlowItem(BaseModel):
    position : int = Field(description="order of object starting at 0")
    attack_technique_id : str
    name: str
    description: str
    context: str = None
    objective: str = None
    variants: list[str] = None

class AttackFlowList(BaseModel):
    tactic_selection: list[tuple[str, str]] = Field(description="attack technique id to attack tactic id mapping using possible_tactics")
    # additional_tactic_mapping: list[tuple[str, str]] = Field(description="the rest of tactic_mapping")
    items : list[AttackFlowItem]
    success: bool = Field(description="determines if there's any valid flow in <extractions>")

    def model_post_init(self, context):
        return super().model_post_init(context)

    @property
    def tactic_mapping(self):
        return dict(self.tactic_selection)

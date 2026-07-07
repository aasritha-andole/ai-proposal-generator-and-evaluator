from typing import TypedDict, Optional, List, Dict


class ProposalState(TypedDict):

    idea: str
    agency: str

    expanded_idea: Optional[Dict]
    guidelines: Optional[Dict]
    proposal: Optional[Dict]
    budget: Optional[Dict]

    proposal_id: Optional[int]   # added for SQLite linking

    rule_score: int
    llm_score: int
    final_score: int

    weak_sections: List[str]

    iteration_count: int  
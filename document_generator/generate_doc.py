from docxtpl import DocxTemplate
from pathlib import Path
from datetime import datetime
import time

# Get project root directory
BASE_DIR = Path(__file__).resolve().parents[1]

# Template directory
TEMPLATE_DIR = BASE_DIR / "templates"

# Output directory (FIXED)
OUTPUT_DIR = Path.cwd() / "outputs"


def generate_document(state):
    try:
        # -----------------------------
        # SAFE INPUT EXTRACTION
        # -----------------------------
        proposal = state.get("proposal", {})
        budget = state.get("budget", {})
        agency = state.get("agency", "").lower()

        # -----------------------------
        # TEMPLATE SELECTION
        # -----------------------------
        template_map = {
            "dst": "dst_template.docx",
            "serb": "serb_template.docx",
            "aicte": "aicte_template.docx"
        }

        if agency not in template_map:
            raise ValueError(f"Unknown agency: {agency}")

        template_path = TEMPLATE_DIR / template_map[agency]

        if not template_path.exists():
            raise FileNotFoundError(f"Template not found at: {template_path}")

        # -----------------------------
        # LOAD TEMPLATE
        # -----------------------------
        doc = DocxTemplate(template_path)

        # -----------------------------
        # CONTEXT DATA
        # -----------------------------
        context = {
            "title": proposal.get("title", ""),
            "abstract": proposal.get("abstract", ""),
            "objectives": "\n".join(proposal.get("objectives", [])),
            "methodology": proposal.get("methodology", ""),
            "expected_results": proposal.get("expected_results", ""),
            "timeline": proposal.get("timeline", ""),

            # Budget
            "personnel_cost": budget.get("personnel_cost", 0),
            "equipment_cost": budget.get("equipment_cost", 0),
            "software_cost": budget.get("software_cost", 0),
            "misc_cost": budget.get("miscellaneous_cost", 0),
            "total_budget": budget.get("total_budget", 0),

            # Evaluation
            "innovation": state.get("innovation", 0),
            "feasibility": state.get("feasibility", 0),
            "clarity": state.get("clarity", 0),
            "final_score": state.get("final_score", 0),

            "generated_time": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        # -----------------------------
        # RENDER DOCUMENT
        # -----------------------------
        doc.render(context)

        # -----------------------------
        # CREATE OUTPUT FOLDER
        # -----------------------------
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        # -----------------------------
        # CREATE FILE PATH
        # -----------------------------
        output_file = OUTPUT_DIR / f"proposal_{agency}_{int(time.time())}.docx"

        # -----------------------------
        # SAVE FILE
        # -----------------------------
        doc.save(str(output_file))

        # -----------------------------
        # DEBUG LOGS
        # -----------------------------
        print("\n🔥 generate_document EXECUTED")
        print("Saved path:", output_file)
        print("Absolute path:", output_file.resolve())
        print("File exists after save:", output_file.exists())

        # -----------------------------
        # ✅ CRITICAL FIX: UPDATE STATE
        # -----------------------------
        state["file_path"] = str(output_file)

        return state

    except Exception as e:
        print("\n❌ ERROR in generate_document:", str(e))

        state["file_path"] = None
        state["error"] = str(e)

        return state
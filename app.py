import json
import google.generativeai as genai
import streamlit as st
gemini_api_key=st.secrets.secret.gemini_api_key
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-1.5-pro')

CONTEXT = "You are an evaluator tasked with reviewing customer support interactions of an airline company to assess the quality of the conversations."
GOAL = """
Your objective is to evaluate the interaction and, using that assessment, rate the conversation on a scale of 1 to 10, where 1 is the lowest and 10 is the highest grade attainable. You are also expected to reason the basis of your given rating.
The conversation should be inspected based on the criteria given in guideline {guidelines}
"""
GUIDELINES = """
Summary: Craft a concise and compelling summary that captures the key aspects of the conversation, highlighting important details effectively.
Tone: Assess the energy of the conversation, noting whether it is warm, neutral, or hostile in nature.
Toxicity: Evaluate for any presence of disrespectful language, inappropriate content, or indications of violence in the conversation.
Trueness: Evaluate whether the response is correct and accurate.
Timeliness: Measure the time taken for a meaningful response in a conversation.
Efficiency: Evaluate how effectively and swiftly the system resolves the user's query, minimizing unnecessary back-and-forth.
User Satisfaction: Measure the user's satisfaction based on their responses and the overall outcome of the conversation.
Empathy: Evaluate how well the system demonstrates understanding and compassion towards the user's situation.
Problem Solving: How effectively the system identifies and resolves the user's problem.
Focus: Evaluate how well the system maintains relevance, ensuring responses stay focused on the user's queries without diverting to unrelated topics.
Adaptiveness: Evaluate the system's ability to adapt to users across different age brackets, races, and regions.
"""

NOTE = """
Remember, while rating the toxicity, evaluate how toxic the conversation is. It is marked on a scale from 1 to 10, where 1 is the lowest toxicity and 10 is the highest toxicity.
For the rating, you can display float values between 1 to 10 based on your evaluation, with a minimum of 1 decimal place and a maximum of 2 decimal places.
"""

FORMAT = """
This is how the format for the response output should look like:
{
 "id": "<conversation_id>",
   "Overall Score": {
    "score": <average_score>,
   },
 "evaluation": {
   "Summary": "<summary of the conversation>",
   "Tone": {
    "score": <score>,
    "reason": "<reason for tone score>"
   },
   "Toxicity": {
    "score": <score>,
    "reason": "<reason for toxicity score>"
   },
   "Trueness": {
    "score": <score>,
    "reason": "<reason for trueness score>"
   },
   "Timeliness": {
    "score": <score>,
    "reason": "<reason for timeliness score>"
   },
   "Efficiency": {
    "score": <score>,
    "reason": "<reason for efficiency score>"
   },
   "User Satisfaction": {
    "score": <score>,
    "reason": "<reason for user satisfaction score>"
   },
   "Empathy": {
    "score": <score>,
    "reason": "<reason for empathy score>"
   },
   "Problem Solving": {
    "score": <score>,
    "reason": "<reason for problem solving score>"
   },
   "Focus": {
    "score": <score>,
    "reason": "<reason for focus score>"
   },
   "Adaptiveness": {
    "score": <score>,
    "reason": "<reason for adaptiveness score>"
   }
 }
}
"""

st.title("Airline customer support Evaluator")
st.subheader("Upload a JSON file for evaluation")

uploaded_file = st.file_uploader("Choose a JSON file", type="json")

if uploaded_file is not None:
    input_json = json.load(uploaded_file)

    complete_prompt = f"{CONTEXT}\n{GOAL.format(guidelines=GUIDELINES)}\n{NOTE}\n{FORMAT}\nYour Input is:\n{json.dumps(input_json)}"

    response = model.generate_content(
        contents=complete_prompt,
        generation_config={'temperature': 0.0}
    )

    if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
        text_content = response.candidates[0].content.parts[0].text
        parsed_json = json.loads(text_content)
    else:
        parsed_json = {"error": "error in parsing"}

    st.subheader("Evaluation Result")
    st.json(parsed_json)

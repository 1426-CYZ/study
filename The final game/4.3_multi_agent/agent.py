from api import call_api
from roles import get_role_prompt


def think(role_name: str, user_question: str) -> str:
    role_prompt = get_role_prompt(role_name)
    messages = [
        {"role": "system", "content": role_prompt},
        {"role": "user", "content": f"用户问：{user_question}\n\n请基于你{role_name}的身份，思考一个初步回答。直接给出回答内容，不要其他说明。"}
    ]
    return call_api(messages)


def advise(role_name: str, user_question: str, other_answer: str, other_role: str) -> str:
    role_prompt = get_role_prompt(role_name)
    messages = [
        {"role": "system", "content": role_prompt},
        {"role": "user", "content": f"""用户问：{user_question}

{other_role}的初步回答：{other_answer}

作为{role_name}，请给{other_role}一个建议，告诉他如何改进这个回答。直接给出建议内容，不要其他说明。"""}
    ]
    return call_api(messages)


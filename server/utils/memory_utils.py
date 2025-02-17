from server.models.user import Messages, UserMessageHistory


async def add_generated_response_to_memory(generated_content, link, question, user_history: UserMessageHistory):
    is_duplicate = False
    for message in user_history.messages:
        if message.question == question and message.answer == generated_content:
            is_duplicate = True
            break
    if not is_duplicate:
        new_message = Messages(question=question,
                            answer=generated_content,
                            video_url=link)
        await new_message.save()
        user_history.messages.append(new_message)
        await user_history.save()
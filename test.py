from tools_agent_email.gmail_tools import GmailTools
from styleAgent import get_style_agent
from agents import Agent, trace, Runner
from controllers.Telegram_Controller import send_message_to_telegram

style_agent = get_style_agent()
instructions = """
The agent receives an array of EmailMessage objects.
For each message in the array, do the following:
Display the subject at the top.
Include the sender's name (sender).
Show the date (date) in a readable format, e.g., 16 November 2025.
Indicate read status: "Read" if star=True, otherwise "Unread".
Indicate if there are attachments: "Yes" if has_attachments=True, otherwise "No".
Include a short snippet (snippet) summarizing the message content.
Arrange all messages in a clean list or table, one after the other.
Ensure all messages are uniform in style; do not show internal fields like msg_id or label.
Return the formatted text to the user in a clear, readable manner.
return name sender and subject and content and date always in hebrew only
"""
style_agent = Agent(name="style_agent", instructions=instructions, model="gpt-4o-mini")


async def get_emails():
    gmail_tool = GmailTools("1122fee0-eece-4e69-9554-b8d4792276ca")
    query = "חשבונית או קבלה"
    try:
        results = gmail_tool.search_emails(
            query=query,
            label="INBOX",
            max_results=3,
            next_page_token=None,
        )
        emails_text = "\n\n".join(
            [
                f"Subject: {e.subject}\nSender: {e.sender}\nSnippet: {e.snippet}"
                for e in results.messages
            ]
        )
        with trace("get_emails"):
            result = await Runner.run(style_agent, emails_text)
            print("result from LLM: ", result.final_output)

        # print(f"Found {results.count} emails")
        # print("results: ", results.messages)
        # with trace("get_emails"):
        #     result = await Runner.run(style_agent, list(results.messages))
        #     print("result from LLM: ", result.final_output)

        await send_message_to_telegram(chat_id=1265060928, text=result.final_output)
        return {"message": "Emails retrieved successfully", "data": results}

    except Exception as e:
        print(f"Error retrieving emails: {e}")
        return {"message": "Error retrieving emails"}


if __name__ == "__main__":
    import asyncio

    asyncio.run(get_emails())

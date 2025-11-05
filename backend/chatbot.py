from openai import OpenAI
from langchain.prompts import PromptTemplate
from backend.retriever import Retriever
from datetime import datetime


class ChatBot():
    """Chatbot Class
    This class encapsulates the functionality of the Resume Chatbot, which interacts with users to provide 
    information about the resume. It leverages various LLM providers (Groq, OpenAI, etc.), LangChain's retrieval tools, 
    and a custom prompt template to generate context-aware responses.
    """

    def __init__(self, parameters: dict[str, any]):
        self.parameters = parameters
        
        # Initialize OpenAI-compatible client for any provider
        self.client = OpenAI(
            api_key=parameters['llm_api_key'],
            base_url=parameters.get('llm_base_url')
        )
        
        self.retrieval_qa_chat_prompt = self.create_prompt()
        self.retriever = Retriever(self.parameters)
        self.vector_store = self.retriever.get_vector_store()
        
        self.chatbot_welcome_message = (
            f"Hi! I'm {parameters['resume_owner_name']}. "
            f"I've created this chatbot to help you learn more about my background, experience, and skills. "
            f"Feel free to ask me anything about my professional journey, projects, or qualifications. "
            f"How can I help you today?"
        )

    def answer(self, query, conversation, conv_last_n_messages=6, fake_conversation=False):
        """Generates a response to the user's query based on the resume data and conversation history.
        
        Args:
            query (str): The user's question or input.
            conversation (list): The history of the conversation between the user and the chatbot.
            conv_last_n_messages (int, optional): The number of recent messages to consider from the 
                conversation history. Defaults to 6.
            fake_conversation (bool, optional): If True, returns a fake response for testing purposes. 
                Defaults to False.
        
        Returns:
            dict: A dictionary containing the user's input, context, and the chatbot's response.
        """
        if fake_conversation:
            # Return fake answer to test the solution without using the paid services 
            result = {
                'input': 'Fake question',
                'context': [],
                'answer': 'This is a fake answer to test the solution without spending LLM tokens...'
            }
            return result
        else:
            # Process the conversation history to provide context for the chatbot
            if len(conversation) > 2:
                # Removing first and last message
                conversation = conversation[1:-1]
                # Keeping the last "conv_last_n_messages" messages of the historic conversation
                if conv_last_n_messages is not None: 
                    conv_last_n_messages = conv_last_n_messages * -1
                    conv_hist = "\n".join([str(entry) for entry in conversation[conv_last_n_messages:]])  
                else:
                    # The entire historic conversation
                    conv_hist = "\n".join([str(entry) for entry in conversation])   
            else:
                conv_hist = 'There is no previous messages'
            
            current_date = datetime.now()
            current_date = current_date.strftime("%B %d, %Y")

            # Search for relevant context from the resume
            search_results = self.vector_store.similarity_search(query, k=3)
            context = "\n\n".join([doc.page_content for doc in search_results])
            
            # Format the prompt with all necessary information
            prompt = self.retrieval_qa_chat_prompt.format(
                context=context,
                history=conv_hist,
                date=current_date,
                resume_owner_name=self.parameters['resume_owner_name'],
                input=query
            )
            
            # Generate response using the LLM
            try:
                response = self.client.chat.completions.create(
                    model=self.parameters['llm_model'],
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant specialized in answering questions about resumes."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=self.parameters.get('llm_temperature', 0),
                    max_tokens=500
                )
                
                answer = response.choices[0].message.content
                
            except Exception as e:
                # Log error and return a user-friendly message
                print(f"Error generating response: {str(e)}")
                answer = f"I apologize, but I encountered an error while processing your question. Please try again or rephrase your question."
            
            result = {
                'input': query,
                'context': search_results,
                'answer': answer
            }
            
            return result
        
    def create_prompt(self):
        """Creates a custom prompt template for the chatbot.
        
        The prompt template instructs the chatbot to answer questions based on the provided context 
        (resume data), conversation history, and user input. It ensures that the chatbot focuses on 
        candidate qualifications, skills, and experiences.
        
        Returns:
            PromptTemplate: A LangChain prompt template for generating responses.
        """
        return PromptTemplate.from_template("""
You are {resume_owner_name}, responding to questions about your professional background and experience.
Answer questions in the FIRST PERSON, as if you are the candidate speaking directly to the recruiter.

IMPORTANT RULES: 
- CRITICAL: Respond in the SAME LANGUAGE as the user's question (French if question is in French, English if in English, etc.)
- Use "I", "my", "me" instead of "the candidate", "he/she", or your name
- DO NOT start your response with greetings like "Bonjour!", "Hello!", "Hi!" - just answer the question directly
- If this is a follow-up question, continue the conversation naturally without re-introducing yourself
- Speak naturally and professionally, as if in an ongoing conversation with a recruiter
- Be confident but humble when discussing your accomplishments
- Answer based solely on the context and conversation history provided below
                                                  
### Context:
Here is the relevant information from your resume:
{context}
Current system Date: {date}

### Conversation History:
These are the previous exchanges in this conversation:
{history}

### User Input:
The user has just asked the following question:
{input}

### Instructions:
Based on the provided context, the conversation history, and the user's latest question, generate a direct and helpful response about your qualifications, skills, experiences, and other background. Answer the question immediately without greetings or pleasantries. Ensure the response is clear, professional, and addresses the specific user query.

If the information requested is not available in the context, politely inform the user that this specific information is not included in your resume.
""")

    def get_chatbot_welcome_message(self):
        """Returns the chatbot's welcome message.
        
        Returns:
            str: A welcome message introducing the chatbot and its purpose.
        """
        return self.chatbot_welcome_message

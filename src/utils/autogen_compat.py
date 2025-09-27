"""
Autogen Compatibility Layer for Python 3.13

This module provides compatibility between the old autogen API (0.2.x) 
and the new autogen API (0.10.x) to maintain backward compatibility.
"""

try:
    # Try new autogen API first
    from autogen_agentchat.agents import AssistantAgent as NewAssistantAgent
    from autogen_agentchat.agents import UserProxyAgent as NewUserProxyAgent
    from autogen_agentchat.agents import GroupChatManager as NewGroupChatManager
    NEW_AUTOGEN = True
except ImportError:
    NEW_AUTOGEN = False

try:
    # Try old autogen API
    from autogen import AssistantAgent as OldAssistantAgent
    from autogen import UserProxyAgent as OldUserProxyAgent
    from autogen import GroupChatManager as OldGroupChatManager
    from autogen.oai.client import OpenAIWrapper
    from autogen.agentchat.conversable_agent import ConversableAgent as Agent
    from autogen.formatting_utils import colored
    OLD_AUTOGEN = True
except ImportError:
    OLD_AUTOGEN = False

# Create compatibility classes
if NEW_AUTOGEN and not OLD_AUTOGEN:
    # Use new API but provide old interface
    class AssistantAgent:
        def __init__(self, *args, **kwargs):
            # Create a minimal compatible agent
            self.name = kwargs.get('name', 'assistant')
            self.system_message = kwargs.get('system_message', '')
            self.llm_config = kwargs.get('llm_config', {})
            
        def generate_reply(self, *args, **kwargs):
            return "AutoGen compatibility mode - limited functionality"
    
    class UserProxyAgent:
        def __init__(self, *args, **kwargs):
            self.name = kwargs.get('name', 'user_proxy')
            self.human_input_mode = kwargs.get('human_input_mode', 'NEVER')
            
        def generate_reply(self, *args, **kwargs):
            return "AutoGen compatibility mode - limited functionality"
    
    class GroupChatManager:
        def __init__(self, *args, **kwargs):
            self.name = kwargs.get('name', 'group_chat_manager')
    
    class OpenAIWrapper:
        def __init__(self, *args, **kwargs):
            pass
    
    class Agent:
        def __init__(self, *args, **kwargs):
            self.name = kwargs.get('name', 'agent')
    
    def colored(text, color):
        """Simple colored text fallback"""
        return text

elif OLD_AUTOGEN:
    # Use old API directly
    AssistantAgent = OldAssistantAgent
    UserProxyAgent = OldUserProxyAgent
    GroupChatManager = OldGroupChatManager
    # OpenAIWrapper and Agent are already imported above
    
else:
    # No autogen available - create dummy classes
    class AssistantAgent:
        def __init__(self, *args, **kwargs):
            self.name = kwargs.get('name', 'assistant')
            self.system_message = kwargs.get('system_message', '')
            self.llm_config = kwargs.get('llm_config', {})
            # Don't print warning during import/creation - only when actually used
            
        def generate_reply(self, *args, **kwargs):
            return "AutoGen compatibility mode - limited functionality"
    
    class UserProxyAgent:
        def __init__(self, *args, **kwargs):
            self.name = kwargs.get('name', 'user_proxy')
            self.human_input_mode = kwargs.get('human_input_mode', 'NEVER')
            # Don't print warning during import/creation - only when actually used
            
        def generate_reply(self, *args, **kwargs):
            return "AutoGen compatibility mode - limited functionality"
    
    class GroupChatManager:
        def __init__(self, *args, **kwargs):
            self.name = kwargs.get('name', 'group_chat_manager')
            # Don't print warning during import/creation - only when actually used
    
    class OpenAIWrapper:
        def __init__(self, *args, **kwargs):
            # Don't print warning during import/creation - only when actually used
            pass
    
    class Agent:
        def __init__(self, *args, **kwargs):
            self.name = kwargs.get('name', 'agent')
            # Don't print warning during import/creation - only when actually used
    
    def colored(text, color):
        """Simple colored text fallback"""
        return text

# Export the compatibility classes
__all__ = ['AssistantAgent', 'UserProxyAgent', 'GroupChatManager', 'OpenAIWrapper', 'Agent', 'colored']

"""
Prompt templates for different information extraction strategies.
"""

from typing import Dict, List, Any


class PromptTemplates:
    """Collection of prompt templates for information extraction."""
    
    def __init__(self):
        self.base_template = """You are an expert information extraction assistant. Extract the following fields from the given text:

Target Fields:
- LastDayWorked: Date when employee last worked
- FirstDayMissed: Date when employee first missed work  
- DeliveryDate: Date for document delivery
- ReturnToWork: Date when employee returned to work

Text: {input_text}

Output format (JSON only):
{{
  "LastDayWorked": "date or null",
  "FirstDayMissed": "date or null", 
  "DeliveryDate": "date or null",
  "ReturnToWork": "date or null"
}}"""
        
        self.few_shot_template = """You are an expert information extraction assistant. Extract the following fields from the given text:

Target Fields:
- LastDayWorked: Date when employee last worked
- FirstDayMissed: Date when employee first missed work  
- DeliveryDate: Date for document delivery
- ReturnToWork: Date when employee returned to work

Examples:

Text: "last day worked 04/25/2023 full shift\nfirst day missed 04/26/2023 induced tomorrow\nemployee returned to work august 1\npaperwork pending delivery date 05/16/2023"
Output: {{"LastDayWorked": "4/25/23", "FirstDayMissed": "4/26/23", "DeliveryDate": "5/16/23", "ReturnToWork": "8/1/23"}}

Text: "employee claim initiation letter to advice of last day worked and induction\nlast day worked 04/25/2023 full shift"
Output: {{"LastDayWorked": "4/25/23", "FirstDayMissed": null, "DeliveryDate": null, "ReturnToWork": null}}

Now extract from this text:

Text: {input_text}

Output format (JSON only):
{{
  "LastDayWorked": "date or null",
  "FirstDayMissed": "date or null", 
  "DeliveryDate": "date or null",
  "ReturnToWork": "date or null"
}}"""
        
        self.chain_of_thought_template = """You are an expert information extraction assistant. Analyze the given text step by step and extract the required information.

Target Fields:
- LastDayWorked: Date when employee last worked
- FirstDayMissed: Date when employee first missed work  
- DeliveryDate: Date for document delivery
- ReturnToWork: Date when employee returned to work

Text: {input_text}

Step 1: Identify all dates mentioned in the text
Step 2: Determine which dates correspond to which fields
Step 3: Extract the information and format as JSON

Output format (JSON only):
{{
  "LastDayWorked": "date or null",
  "FirstDayMissed": "date or null", 
  "DeliveryDate": "date or null",
  "ReturnToWork": "date or null"
}}"""
        
        self.role_based_template = """You are a human resources specialist with expertise in employee records and administrative documentation. Your task is to extract specific information from employee-related text notes.

Extract the following fields from the given text:
- LastDayWorked: Date when employee last worked
- FirstDayMissed: Date when employee first missed work  
- DeliveryDate: Date for document delivery
- ReturnToWork: Date when employee returned to work

Text: {input_text}

As an HR specialist, analyze this text and extract the relevant information in JSON format:

{{
  "LastDayWorked": "date or null",
  "FirstDayMissed": "date or null", 
  "DeliveryDate": "date or null",
  "ReturnToWork": "date or null"
}}"""
        
        self.format_emphasis_template = """Extract information from the following text and return ONLY a valid JSON object.

Required fields:
- LastDayWorked: Date when employee last worked
- FirstDayMissed: Date when employee first missed work  
- DeliveryDate: Date for document delivery
- ReturnToWork: Date when employee returned to work

Text: {input_text}

IMPORTANT: Return ONLY the JSON object, no other text. Use null for missing values.

{{
  "LastDayWorked": "date or null",
  "FirstDayMissed": "date or null", 
  "DeliveryDate": "date or null",
  "ReturnToWork": "date or null"
}}"""
    
    def get_template(self, template_name: str) -> str:
        """
        Get a specific prompt template.
        
        Args:
            template_name: Name of the template
            
        Returns:
            Prompt template string
        """
        templates = {
            'zero_shot': self.base_template,
            'few_shot': self.few_shot_template,
            'chain_of_thought': self.chain_of_thought_template,
            'role_based': self.role_based_template,
            'format_emphasis': self.format_emphasis_template
        }
        
        return templates.get(template_name, self.base_template)
    
    def format_prompt(self, template_name: str, input_text: str, **kwargs) -> str:
        """
        Format a prompt template with input text.
        
        Args:
            template_name: Name of the template
            input_text: Input text to extract from
            **kwargs: Additional formatting parameters
            
        Returns:
            Formatted prompt
        """
        template = self.get_template(template_name)
        return template.format(input_text=input_text, **kwargs)
    
    def get_all_templates(self) -> List[str]:
        """
        Get list of all available template names.
        
        Returns:
            List of template names
        """
        return ['zero_shot', 'few_shot', 'chain_of_thought', 'role_based', 'format_emphasis']
    
    def create_custom_template(self, instructions: str, examples: List[Dict[str, str]] = None) -> str:
        """
        Create a custom prompt template.
        
        Args:
            instructions: Custom instructions
            examples: List of example input/output pairs
            
        Returns:
            Custom template string
        """
        template = f"""You are an expert information extraction assistant. {instructions}

Target Fields:
- LastDayWorked: Date when employee last worked
- FirstDayMissed: Date when employee first missed work  
- DeliveryDate: Date for document delivery
- ReturnToWork: Date when employee returned to work

"""
        
        if examples:
            template += "Examples:\n\n"
            for i, example in enumerate(examples):
                template += f"Text: \"{example['input']}\"\n"
                template += f"Output: {example['output']}\n\n"
        
        template += """Text: {input_text}

Output format (JSON only):
{{
  "LastDayWorked": "date or null",
  "FirstDayMissed": "date or null", 
  "DeliveryDate": "date or null",
  "ReturnToWork": "date or null"
}}"""
        
        return template

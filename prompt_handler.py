# prompt_handler.py
def create_summary_prompt(extracted_text):
    return f"""
    Create an executive summary of this RFP document tailored for an executive architectural designer. Include key dates (issue date, response/submission due date, selection date, other important dates and times), a project overview, the scope of work, a list of deliverables, Selection Criteria, and other important information. Conclude with a concise and brief one-sentence summary identifying specific areas in the RFP where it may align with core values, such as Design Excellence, Living Design, Sustainability, Resilience, Research, Diversity and Inclusion, Social Purpose, Well-Being, and Technology, with specific examples from the document.

    RFP Document Text:
    {extracted_text}
    """

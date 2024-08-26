

GRADIENT_TEXT = """<div style="display: flex; align-items: center; padding: 20px; background: linear-gradient(to right, #FFD4DD , #000395); border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <div style="flex-shrink: 0; margin-right: 20px;">
                <img src="{0}" style="width: 150px; height: 150px; border-radius: 50%; border: 4px solid white; box-shadow: 0 0 8px rgba(0, 0, 0, 0.3);">
            </div>
            <div style="flex-grow: 1;">
                <h1 style="font-size: 3em; margin-bottom: 0; color: #e0fbfc;">{1}</h1>
                <p style="font-size: 1.5em; margin-top: 0.5em; color: white;">{2}</p>
            </div>
        </div>"""   


CONTANT_STRUCTURE = """
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">

<div class="contact-bar">
    <div class="contact-item">
        <i class="fas fa-phone contact-icon" style="color: #0073b1;"></i>
        <p><a href="{0}" class="contact-link">{0}</a></p>
    </div>
    <div class="contact-item">
        <i class="fas fa-envelope contact-icon" style="color: #0073b1;"></i>
        <p><a href="mailto:{1}" class="contact-link">{1}</a></p>
    </div>
    <div class="contact-item">
        <i class="fab fa-linkedin contact-icon" style="color: #0073b1;"></i>
        <p><a href="{2}" class="contact-link" target="_blank">LinkedIn</a></p>
    </div>
    <div class="contact-item">
        <i class="fab fa-youtube contact-icon" style="color: #FF0000;"></i>
        <p><a href="{3}" class="contact-link" target="_blank">Youtube</a></p>
    </div>
    <div class="contact-item">
        <i class="fab fa-medium contact-icon" style="color: #00ab6c;"></i>
        <p><a href="{4}" class="contact-link" target="_blank">Medium</a></p>
    </div>
</div>
        """

SKILL_STRUCTURE = {
    "langchain":"""
            <div style="text-align: center;">
            <img src="https://blogs.perficient.com/files/lanchain.png" width="150">
            <div style="text-align: left; margin-top: 10px;">Langchain</div>
             </div>
            """,

    "azure": """
        <div style="text-align: center;">
        <img src="https://i0.wp.com/securityaffairs.com/wp-content/uploads/2019/06/microsoft-azure.png?fit=770%2C480&ssl=1" width="130" height="120">
        <div style="text-align: left; margin-top: 10px;">Azure</div>
            </div>
        """,

    "sklearn" :"""
        <div style="text-align: center;">
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRNsNsCUnCK9dU4ADTVmRc0fs0KpHJwWFNJjQ&s" width="120">
        <div style="text-align: left; margin-top: 10px;">Scikit-Learn</div>
            </div>
        """
}

WORK_EXP_STRUCTURE = """
            <div class="experience-card">
                <div class="experience-header">
                    {0} at {1}
                </div>
                <div class="experience-details">
                    <strong>Start Date:</strong> {2}<br>
                    <strong>End Date:</strong> {3}
                </div>
                <div class="experience-responsibilities">
                    <strong>Responsibilities:</strong>
                    <ul>
            """



from fpdf import FPDF
from tkinter import messagebox
def createsessionplanPDF(jsonobj, customer_name,directory):

    # "P" for portrait
    # "mm" for measurement type
    # "Letter" for format
    pdf = FPDF("P", "mm", "Letter")


    # add a page
    pdf.add_page()

    # specify font
    # "B" (Bold) "U" (Underline) "I" (Italics), "" (Regular)
    pdf.set_font("helvetica", "B", 16)

    
    pdf.cell(40,10,f"Session plan for {customer_name}", ln=True)
    pdf.cell(40,10,f"Last Modified: {str(jsonobj['timestamp'])}", ln=True)
    pdf.cell(40,10,f"Planned Session Date: {str(jsonobj['planned_date'])}", ln=True)



    for circuit in jsonobj["circuits"]:
        pdf.set_font("helvetica", "B", 13)

        # add text
        # w = width of cell (0 = entire page)
        # h = height of cell (0 = entire page)
        pdf.cell(40,10,"", ln=True)

        pdf.cell(40,10,circuit["circuit_name"], ln=True)

        for superset in circuit["supersets"]:
            pdf.set_font("helvetica", "U", 13)

            pdf.cell(40,10,superset["superset_name"], ln=True)

            for i,set in enumerate(superset["sets"]):
                pdf.set_font("helvetica", "", 13)
                pdf.cell(40,10,f"Set {str(i+1)}: {set['name']}", ln=True)

    output_directory = directory + "/SessionPlan_" + customer_name + "_PlannedDate_" + str(jsonobj['planned_date']).replace("/",".").replace(":",".") + ".pdf"
    pdf.output(output_directory)

    messagebox.showinfo(title="Completed", message=f"Session plan was written to {output_directory}")

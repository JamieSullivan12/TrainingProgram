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

    # loop through circuits
    for circuit in jsonobj["circuits"]:
        pdf.set_font("helvetica", "B", 13) # bolded
        pdf.cell(40,10,"", ln=True) # empty line
        pdf.cell(40,10,circuit["circuit_name"], ln=True) # circuit heading
        
        # loop through supersets
        for superset in circuit["supersets"]:
            pdf.set_font("helvetica", "U", 13) # underlined
            pdf.cell(40,10,superset["superset_name"], ln=True) # superset heading

            # loop through sets
            for i,set in enumerate(superset["sets"]):
                pdf.set_font("helvetica", "", 13)
                
                # differentiating between reps, time or distance-based exercises (this information will be added to the PDF)
                reps = set['reps']
                time = set['time']
                distance = set['distance']
                suffix_text = ""
                if str(reps) != "0":
                    suffix_text = f"Reps: {reps}"
                elif str(time) != "0":
                    suffix_text = f"Time: {time} s"
                elif str(distance) != "0":
                    suffix_text = f"Distance: {distance} m"
                # add set to PDF    
                pdf.cell(40,10,f"Set {str(i+1)}: {set['name']} - {suffix_text}", ln=True)

    output_directory = directory + "/SessionPlan_" + customer_name + "_PlannedDate_" + str(jsonobj['planned_date']).replace("/",".").replace(":",".") + ".pdf"
    pdf.output(output_directory)

    messagebox.showinfo(title="Completed", message=f"Session plan was written to {output_directory}")

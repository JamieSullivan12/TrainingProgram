from fpdf import FPDF
from tkinter import messagebox
def createsessionplanPDF(trainingplan, customer_name, directory):

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
    pdf.cell(40,10,f"Last Modified: {str(trainingplan.timestamp)}", ln=True)
    pdf.cell(40,10,f"Planned Training Plan Date: {str(trainingplan.planned_date)}", ln=True)

    # loop through circuits
    for circ_count, circuit in enumerate(trainingplan.circuits):
        pdf.set_font("helvetica", "B", 13) # bolded
        pdf.cell(40,10,"", ln=True) # empty line
        pdf.cell(40,10,f"Circuit {circ_count+1}", ln=True) # circuit heading
        
        # loop through stations
        for sup_count, station in enumerate(circuit.stations):
            pdf.set_font("helvetica", "U", 13) # underlined
            pdf.cell(40,10,f"Station {sup_count+1}", ln=True) # station heading

            # loop through sets
            for set_count,set in enumerate(station.sets):
                pdf.set_font("helvetica", "", 13)
                
                length = set.length

                if set.overridename != "": 
                    setname=set.overridename
                else:
                    setname=set.exercise_obj.descriptor
                
                if set.overridelength != str(0): 
                    suffix_text = set.overridelength
                else:
                    suffix_text = ""
                    if set.exercise_obj.format == 1:
                        suffix_text = f"Reps: {length}"
                    elif set.exercise_obj.format == 2:
                        suffix_text = f"Time: {length} s"
                    elif set.exercise_obj.format == 3 or set.exercise_obj.format == 4:
                        suffix_text = f"Distance: {length} m"
                # add set to PDF    
                pdf.cell(40,10,f"Set {str(set_count+1)}: {setname} - {suffix_text}", ln=True)

    output_directory = directory + "/SessionPlan_" + customer_name + "_PlannedDate_" + str(trainingplan.planned_date).replace("/",".").replace(":",".") + ".pdf"
    pdf.output(output_directory)

    messagebox.showinfo(title="Completed", message=f"Session plan was written to {output_directory}")
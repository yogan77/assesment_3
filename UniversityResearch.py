import json

def calculate_score(faculty):
    return (0.4 * faculty["Publications"]) + (0.3 * faculty["H_index"]) + (0.3 * faculty["Collaboration_Score"])

def process_grants(faculty_list):
    valid_data = []
    for f in faculty_list:
        try:
            budget = float(f["Project_Budget_Requested"])
            if budget < 0:
                raise ValueError("Negative budget")
            f["Clean_Budget"] = budget
            f["Research_Score"] = calculate_score(f)
            # Allocation rule example: Grant scaled by score if budget valid
            f["Allocated_Grant"] = f["Clean_Budget"] * (f["Research_Score"] / 100)
            valid_data.append(f)
        except (ValueError, TypeError):
            print(f"Invalid budget handled for Faculty ID: {f.get('Faculty_ID')}")

    ranked = sorted(valid_data, key=lambda x: x["Research_Score"], reverse=True)
  
    above_100k = [f for f in ranked if f["Allocated_Grant"] > 100000]
    
    dept_funding = {}
    for f in ranked:
        dept = f["Department"]
        dept_funding[dept] = dept_funding.get(dept, 0) + f["Allocated_Grant"]
    max_dept = max(dept_funding, key=dept_funding.get) if dept_funding else None
    
    avg_score = sum(f["Research_Score"] for f in ranked) / len(ranked) if ranked else 0
    
    top_performer = ranked[0] if ranked else None

    with open("rankings.json", "w") as file:
        json.dump(ranked, file, indent=4)
      
    with open("rankings.json", "r") as file:
        saved_data = json.load(file)

    return ranked, above_100k, max_dept, avg_score, top_performer, saved_data

data = [
    {"Faculty_ID": "F01", "Faculty_Name": "Alice", "Department": "CS", "Publications": 10, "H_index": 8, "Project_Budget_Requested": 250000, "Collaboration_Score": 9},
    {"Faculty_ID": "F02", "Faculty_Name": "Bob", "Department": "EE", "Publications": 5, "H_index": 4, "Project_Budget_Requested": "invalid", "Collaboration_Score": 5},
    {"Faculty_ID": "F03", "Faculty_Name": "Charlie", "Department": "CS", "Publications": 15, "H_index": 12, "Project_Budget_Requested": 400000, "Collaboration_Score": 10}
]

if __name__ == "__main__":
    res = process_grants(data)
    print("Top Performer:", res[4]["Faculty_Name"] if res[4] else "None")
    print("Max Funded Dept:", res[2])

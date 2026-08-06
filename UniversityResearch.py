import json

projects = [
    {
        "Faculty ID": "F001",
        "Faculty Name": "Dr. Smith",
        "Department": "Computer Science",
        "Publications": 20,
        "H-index": 12,
        "Project Budget Requested": 120000,
        "Industry Collaboration Score": 80
    },
    {
        "Faculty ID": "F002",
        "Faculty Name": "Dr. Jones",
        "Department": "Mechanical",
        "Publications": 10,
        "H-index": 5,
        "Project Budget Requested": 90000,
        "Industry Collaboration Score": 50
    },
    {
        "Faculty ID": "F003",
        "Faculty Name": "Dr. Lee",
        "Department": "Computer Science",
        "Publications": 30,
        "H-index": 20,
        "Project Budget Requested": 150000,
        "Industry Collaboration Score": 90
    }
]

def validate_budget(budget):
    try:
        b = float(budget)
        if b < 0:
            raise ValueError("Budget cannot be negative.")
        return b
    except (ValueError, TypeError):
        print(f"Invalid budget value: {budget}. Setting budget to $0.0.")
        return 0.0
def process_faculty_data(data):
    dept_funding = {}
    total_score = 0
    
    for p in data:
        p["Project Budget Requested"] = validate_budget(p["Project Budget Requested"])
        
        p["Research Score"] = (0.4 * p["Publications"]) + (0.3 * p["H-index"]) + (0.3 * p["Industry Collaboration Score"])
        total_score += p["Research Score"]
        
        if p["Research Score"] > 25:
            p["Grant Allocated"] = p["Project Budget Requested"]
        else:
            p["Grant Allocated"] = p["Project Budget Requested"] * 0.5
            
        dept = p["Department"]
        dept_funding[dept] = dept_funding.get(dept, 0) + p["Grant Allocated"]

    ranked_faculty = sorted(data, key=lambda x: x["Research Score"], reverse=True)
    for i, faculty in enumerate(ranked_faculty, start=1):
        faculty["Rank"] = i

    print("--- Grants Above $100,000 ---")
    for f in ranked_faculty:
        if f["Grant Allocated"] > 100000:
            print(f"{f['Faculty Name']}: ${f['Grant Allocated']:.2f}")

    max_dept = max(dept_funding, key=dept_funding.get) if dept_funding else None
    print(f"\nDepartment with Max Funding: {max_dept} (${dept_funding[max_dept]:.2f})")

    avg_score = total_score / len(data) if data else 0
    print(f"Average Research Score: {avg_score:.2f}")

    top_performer = ranked_faculty[0] if ranked_faculty else None
    print(f"Top Performer: {top_performer['Faculty Name']} (Score: {top_performer['Research Score']:.2f})")

    return ranked_faculty

def save_rankings(ranked_data, filename="rankings.json"):
    with open(filename, "w") as f:
        json.dump(ranked_data, f, indent=4)
    print(f"\nRankings saved to {filename}.")

def read_rankings(filename="rankings.json"):
    with open(filename, "r") as f:
        data = json.load(f)
    print(f"\n--- Reading Rankings Back from {filename} ---")
    for item in data:
        print(f"Rank {item['Rank']}: {item['Faculty Name']} - Score: {item['Research Score']:.2f}")

processed_data = process_faculty_data(projects)
save_rankings(processed_data)
read_rankings()

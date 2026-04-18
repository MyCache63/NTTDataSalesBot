#!/usr/bin/env python3
"""Generate ~100 fictitious ServiceNow IT service tickets for Trinity Health demo."""

import csv
import random
from datetime import datetime, timedelta

random.seed(42)

# --- Reference data ---

LOCATIONS = [
    "Trinity Health HQ - Livonia, MI",
    "St. Joseph Mercy - Ann Arbor, MI",
    "Mercy Health - Grand Rapids, MI",
    "Mount Carmel - Columbus, OH",
    "Saint Alphonsus - Boise, ID",
    "Holy Cross Hospital - Fort Lauderdale, FL",
    "Loyola Medicine - Maywood, IL",
    "St. Francis Hospital - Indianapolis, IN",
    "MercyOne - Des Moines, IA",
    "St. Peter's Health Partners - Albany, NY",
]

CALLERS = [
    "Jennifer Martinez, RN", "Dr. Robert Chen", "Amanda Williams", "David Johnson, PA",
    "Sarah Thompson", "Michael O'Brien", "Lisa Patel, RN", "James Wilson",
    "Karen Rodriguez", "Dr. Emily Foster", "Thomas Brown", "Patricia Davis, NP",
    "Christopher Lee", "Michelle Garcia", "Daniel Kim", "Rebecca Turner, RN",
    "Andrew Clark", "Stephanie Moore", "Brian Anderson", "Dr. Laura Nguyen",
    "Jessica White", "Mark Taylor", "Nicole Jackson", "Ryan Harris, PA",
    "Kimberly Martin", "Dr. Steven Wright", "Ashley Robinson", "Kevin Lewis",
    "Samantha Young", "Dr. William Hall", "Megan Allen", "Eric Sanchez",
    "Heather King", "Jason Scott", "Tiffany Green", "Dr. Rachel Adams",
    "Brandon Baker", "Amber Nelson", "Justin Carter", "Christina Mitchell",
]

TECHNICIANS = [
    "Alex Ramirez", "Tony Baxter", "Priya Sharma", "Derek Owens",
    "Linda Chow", "Marcus Jenkins", "Sara Fitzgerald", "Raj Patel",
    "Beth Kowalski", "Darnell Washington", "Yuki Tanaka", "Connor Murphy",
]

ASSIGNMENT_GROUPS = [
    "Service Desk - Tier 1",
    "Desktop Support - Tier 2",
    "Network Operations",
    "Clinical Applications Support",
    "Server & Infrastructure",
    "Identity & Access Management",
    "Telecom & VoIP",
    "Endpoint Security",
    "Database Administration",
    "EHR Support - Epic",
]

CONTACT_TYPES = ["Phone", "Self-Service Portal", "Email", "Chat", "Walk-in"]

CATEGORIES = {
    "Hardware": ["Desktop", "Laptop", "Printer", "Monitor", "Peripheral", "Mobile Device", "Thin Client"],
    "Software": ["Operating System", "Office Suite", "Clinical Application", "Browser", "Antivirus", "Imaging Software"],
    "Network": ["Connectivity", "VPN", "WiFi", "DNS", "Firewall", "Bandwidth"],
    "Account/Access": ["Password Reset", "Account Lockout", "New Account", "Permission Change", "MFA", "Badge Access"],
    "Email & Collaboration": ["Outlook", "Teams", "SharePoint", "OneDrive", "Distribution List"],
    "EHR/Clinical Systems": ["Epic", "CPOE", "Clinical Documentation", "Lab Integration", "Pharmacy", "Radiology PACS"],
    "Telephony": ["Desk Phone", "Voicemail", "Call Routing", "Pager", "On-Call System"],
    "Database": ["Performance", "Connectivity", "Backup/Restore", "Query", "Replication"],
}

BUSINESS_SERVICES = [
    "Patient Care - Inpatient",
    "Patient Care - Outpatient",
    "Emergency Department",
    "Laboratory Services",
    "Pharmacy Operations",
    "Radiology & Imaging",
    "Administrative Operations",
    "Revenue Cycle / Billing",
    "Human Resources",
    "Supply Chain",
]

CONFIGURATION_ITEMS = {
    "Hardware": ["Dell OptiPlex 7090", "HP EliteBook 840", "Zebra ZD420 Label Printer", "HP LaserJet M607",
                 "Dell U2722D Monitor", "Lenovo ThinkPad T14", "Dell Wyse 5070 Thin Client", "iPad Pro 12.9"],
    "Software": ["Windows 11 Enterprise", "Microsoft 365 Apps", "Epic Hyperspace 2024", "Adobe Acrobat Pro",
                 "Citrix Workspace", "Chrome Enterprise", "CrowdStrike Falcon"],
    "Network": ["Cisco Catalyst 9300", "Aruba AP-535", "Palo Alto PA-5260", "Cisco AnyConnect VPN",
                "Cisco ISE", "F5 BIG-IP"],
    "Account/Access": ["Active Directory", "Azure AD / Entra ID", "Imprivata OneSign", "Duo MFA",
                       "RFID Badge System", "CyberArk PAM"],
    "Email & Collaboration": ["Exchange Online", "Microsoft Teams", "SharePoint Online", "OneDrive for Business"],
    "EHR/Clinical Systems": ["Epic Hyperspace", "Epic Haiku (Mobile)", "Epic Canto", "Nuance PowerScribe",
                             "PACS - Sectra", "Pyxis MedStation"],
    "Telephony": ["Cisco UCM", "Cisco Jabber", "Vocera Badge", "Amcom On-Call"],
    "Database": ["SQL Server 2019", "Oracle 19c", "MongoDB Atlas", "Azure SQL"],
}

STATES = ["New", "In Progress", "On Hold", "Resolved", "Closed"]
RESOLUTION_CODES = ["Solved (Permanently)", "Solved (Workaround)", "Not Solved", "Duplicate", "Caller Withdrew"]
PRIORITIES = ["1 - Critical", "2 - High", "3 - Moderate", "4 - Low"]
IMPACTS = ["1 - High", "2 - Medium", "3 - Low"]
URGENCIES = ["1 - High", "2 - Medium", "3 - Low"]

# --- Ticket templates with sentiment ---
# Each is (short_desc, description, customer_comment, sentiment_label)
# sentiment: negative, neutral, positive

TICKET_TEMPLATES = [
    # NEGATIVE - frustrated, angry, urgent complaints
    (
        "Epic Hyperspace keeps crashing mid-charting",
        "Epic Hyperspace freezes and crashes every 15-20 minutes when I'm charting patient notes in the inpatient module. I lose all my unsaved work each time. This has been happening for 3 days now. I've already restarted my workstation twice today.",
        "This is COMPLETELY unacceptable. I've lost patient notes THREE times today. I'm a nurse with 12 patients and I cannot keep re-entering chart data. Someone needs to fix this NOW or I'm calling my director.",
        "negative"
    ),
    (
        "VPN drops connection every 10 minutes from home",
        "When working remotely via Cisco AnyConnect VPN, the connection drops approximately every 10 minutes. I have to re-authenticate each time. My home internet is stable — I've tested with speed tests and other apps work fine.",
        "I've called about this FOUR times now and nobody has fixed it. I can't do my job from home like this. Every time I call I get a different person who makes me run the same diagnostics. This is beyond frustrating.",
        "negative"
    ),
    (
        "Cannot print patient wristbands - printer jammed",
        "Zebra wristband printer on 4th floor nursing station is jammed and not responding. We've tried clearing the jam and power cycling. Registration cannot print patient wristbands for new admissions.",
        "We have patients waiting in admissions with NO wristbands. This is a patient safety issue. We need someone up here IMMEDIATELY, not in 4 hours. Last time this happened we waited all day.",
        "negative"
    ),
    (
        "Locked out of account for the third time this week",
        "My Active Directory account keeps getting locked out. I change my password, it works for a day, then locks again. I suspect an old session or cached credentials somewhere but I can't find it.",
        "I am so tired of calling about this. Every single time I'm told it's fixed and then the next morning I'm locked out again. I've wasted hours this week just trying to log in. This is ridiculous.",
        "negative"
    ),
    (
        "Outlook not syncing — missing critical emails",
        "Outlook desktop client stopped syncing about 6 hours ago. I can see new emails in OWA but they don't appear in my desktop app. I've tried restarting Outlook and repairing the profile.",
        "I missed an urgent email from a physician about a patient medication change because of this. This is not just an inconvenience — it's potentially dangerous in a healthcare setting. Please escalate.",
        "negative"
    ),
    (
        "Shared drive access removed without notice",
        "I no longer have access to the \\\\fileserver\\deptshare\\nursing drive that I've used for 3 years. No one notified me of any changes. I need files from there for today's staff meeting.",
        "Why was my access removed with no warning? I have a department meeting in 2 hours and all my presentation files are on that drive. Nobody in IT seems to know why this happened. Very poor communication.",
        "negative"
    ),
    (
        "New laptop is slower than my 5-year-old machine",
        "Received my new HP EliteBook replacement last week. It takes 4-5 minutes to boot, applications take forever to open, and Epic is noticeably slower than on my old Dell. This is supposed to be an upgrade.",
        "I waited 3 months for this laptop 'upgrade' and it's significantly worse than what I had. I specifically asked if it would be faster and was told yes. I want my old machine back or a different replacement. Very disappointed.",
        "negative"
    ),
    (
        "Badge tap not working at any door",
        "My proximity badge stopped working at all badge-access doors throughout the facility as of this morning. I can't get into the med room, supply closet, or restricted areas. I've been borrowing colleagues' badges.",
        "I'm a nurse and I NEED access to the medication rooms. Having to borrow badges is a compliance violation. I've been standing at doors waiting for people to let me in for my entire shift. Unacceptable.",
        "negative"
    ),
    (
        "Teams calls dropping — can't attend meetings",
        "Microsoft Teams calls disconnect after 2-3 minutes. Audio cuts out first, then the call drops entirely. This happens on both WiFi and ethernet. Browser-based Teams has the same issue.",
        "I've missed or been dropped from three important patient care coordination meetings today. My manager is questioning my attendance. This needs to be fixed TODAY — I cannot keep missing meetings.",
        "negative"
    ),
    (
        "Duplicate patient records appearing in Epic",
        "We're seeing what appear to be duplicate MRNs for at least 4 patients on our unit. The records have slightly different demographics but same DOB and similar names. This is a data integrity concern.",
        "This is a SERIOUS patient safety issue. If medications or allergies are split across duplicate records, we could make a critical error. I need this escalated to Epic support immediately, not sitting in a queue.",
        "negative"
    ),
    (
        "Monitor flickering constantly — causing headaches",
        "My Dell monitor flickers intermittently throughout the day. Some days it's every few seconds, other days every few minutes. It's been happening for 2 weeks and is causing eye strain and headaches.",
        "I've had to take Advil every day this week because of the headaches from this monitor. I submitted a ticket 2 weeks ago and heard nothing. My productivity is suffering and so is my health.",
        "negative"
    ),
    (
        "Pager not receiving critical lab alerts",
        "My Amcom pager has not been receiving critical lab value alerts since yesterday. I only discovered this when a colleague verbally informed me of a critical potassium result. Other pages seem to come through fine.",
        "A patient could have been seriously harmed because I didn't receive a critical lab alert. This is not a minor IT inconvenience — this is a patient safety emergency. I need this fixed within the hour.",
        "negative"
    ),
    (
        "Software update broke my workflow completely",
        "After the overnight Windows update, several of my desktop shortcuts are gone, my default printer changed, and Citrix won't launch. I've been unable to access any clinical applications for 2 hours.",
        "Every time IT pushes an update, something breaks. I spend more time on the phone with the help desk than I do with patients. Who tests these updates before pushing them? Clearly nobody who actually uses these systems.",
        "negative"
    ),
    (
        "WiFi dead zone in new outpatient wing",
        "There is no WiFi coverage in rooms 302-310 of the new outpatient wing. Clinicians cannot access Epic on their mobile devices in these rooms. We've been open for a week with this issue.",
        "How did we open an entire wing of a hospital without WiFi? Providers are having to walk to the hallway to look things up and then walk back. This is 2026, not 1996. Extremely poor planning.",
        "negative"
    ),
    (
        "Citrix session keeps freezing during patient intake",
        "Citrix Workspace sessions freeze for 30-60 seconds multiple times per hour. When it unfreezes, keystrokes entered during the freeze all appear at once, often in the wrong fields. Happening on all thin clients in our area.",
        "Patient intake is taking twice as long because of this freezing. We have a waiting room full of frustrated patients and I look incompetent sitting here waiting for my screen to unfreeze. How long has this been a known issue?",
        "negative"
    ),
    (
        "Wrong user profile loaded on shared workstation",
        "When I log into the shared workstation at the 3rd floor nursing station, it loads a different user's profile. I can see their desktop, their files, their bookmarks. This is a privacy and security concern.",
        "I could see another employee's personal files and saved passwords. This is a HIPAA concern if patient data was accessible too. I didn't touch anything but this needs to be fixed and investigated immediately.",
        "negative"
    ),
    (
        "Fax server down — can't send referrals",
        "The fax server has been down since 7 AM. We cannot send patient referrals, prior authorizations, or lab results to external providers. This is impacting patient care for the entire clinic.",
        "We have 15+ referrals that need to go out today and the fax server is STILL down at 2 PM. Patients are going to have delayed care because of this. Why don't we have a backup? This is healthcare, not a pizza shop.",
        "negative"
    ),
    (
        "Cannot access lab results in Epic — timeout errors",
        "When clicking on Lab Results in Epic, the system times out after about 60 seconds and returns an error. This is happening for all patients, not just one record. Started about an hour ago.",
        "I need to review labs before I can discharge patients. I currently have 3 patients waiting for discharge and I can't verify their lab results. This is causing a bed flow crisis on my unit.",
        "negative"
    ),

    # NEUTRAL - factual, straightforward reporting
    (
        "Password reset needed — account expired",
        "My password expired over the weekend and I need it reset. Employee ID: 4458812. I'm at the front desk in outpatient registration and need access to start my shift.",
        "Thank you, please let me know when it's ready.",
        "neutral"
    ),
    (
        "Request new monitor for workstation",
        "Requesting a second monitor for my desk in the Revenue Cycle department. My manager (Karen Rodriguez) has approved the purchase. I currently have one 24-inch monitor and need a second for billing workflows.",
        "Please let me know the expected delivery timeline.",
        "neutral"
    ),
    (
        "Need access to SharePoint site for quality department",
        "I recently transferred to the Quality Improvement department and need access to their SharePoint site at /sites/QualityImprovement. My manager is Dr. Emily Foster who can approve.",
        "Transferred from Nursing Informatics last week. My manager said to open a ticket for this.",
        "neutral"
    ),
    (
        "Printer toner replacement needed — 2nd floor admin",
        "The HP LaserJet on the 2nd floor administrative area is showing 'Toner Low' and print quality has degraded. Requesting toner replacement. Printer asset tag: PRN-2F-004.",
        "Not urgent but we'll need it by end of week for month-end reports.",
        "neutral"
    ),
    (
        "New hire setup — starting Monday",
        "New employee starting Monday 4/21. Name: Jordan Phillips. Title: Medical Assistant. Department: Cardiology Outpatient. Manager: Dr. Robert Chen. Will need standard clinical workstation setup, Epic access (ambulatory), and email.",
        "HR onboarding form attached. Please confirm when setup is complete.",
        "neutral"
    ),
    (
        "Requesting VPN access for remote work",
        "I've been approved for 2 days/week remote work starting next month. Requesting Cisco AnyConnect VPN access. My manager (James Wilson) has approved. I have a Trinity Health-issued laptop.",
        "IT security training is already completed. Certificate attached.",
        "neutral"
    ),
    (
        "Conference room projector not displaying",
        "The projector in Conference Room B (2nd floor) is not displaying from any input source. The power light is on but no image appears on screen. We have a meeting at 2 PM today.",
        "Can someone look at this before 2 PM if possible? If not, we can relocate the meeting.",
        "neutral"
    ),
    (
        "Software installation request — Adobe Acrobat Pro",
        "Requesting installation of Adobe Acrobat Pro on my workstation. I need to edit and digitally sign PDF documents for compliance reporting. Cost center: 44120. Manager approval: attached.",
        "Standard license from our enterprise agreement should work.",
        "neutral"
    ),
    (
        "Email distribution list update",
        "Please add the following employees to the 'Cardiology-AllStaff' distribution list: Jordan Phillips (jphillips@trinityhealth.org) and Maria Santos (msantos@trinityhealth.org). Both are new hires in Cardiology.",
        "Their manager Dr. Chen has approved. Thank you.",
        "neutral"
    ),
    (
        "Network port activation — new office",
        "Need network port activated in office 415B (4th floor, east wing). Port label reads 4E-415B-01. We're setting up a new workstation for a transferred physician. Ethernet only — no WiFi needed at the desk.",
        "Not urgent. The physician starts in the new office next Monday.",
        "neutral"
    ),
    (
        "Desk phone not ringing — voicemail works",
        "My desk phone (ext. 4412) doesn't ring for incoming calls. Calls go directly to voicemail. I can make outgoing calls fine. The phone display shows it's registered normally.",
        "I noticed it yesterday but wasn't sure if it was a temporary issue. Confirmed today it's still happening.",
        "neutral"
    ),
    (
        "Request to add printer to my workstation",
        "I need the 3rd floor Radiology printer (PRN-3F-RAD-01) added to my workstation so I can print reports locally. I'm in room 312. Currently my only option is the printer down the hall.",
        "Low priority. Just a convenience request.",
        "neutral"
    ),
    (
        "MFA token expired — need replacement",
        "My Duo MFA hardware token has expired. The serial number is DUO-TH-88412. Requesting a replacement token. I'm on-site at St. Joseph Mercy and can pick up a new one from IT.",
        "I can use the Duo mobile app as a temporary workaround in the meantime.",
        "neutral"
    ),
    (
        "Laptop docking station not detected",
        "My HP docking station is no longer being detected by my laptop. External monitors and USB peripherals don't connect when docked. I've tried different cables and power cycling the dock.",
        "I have a USB-C adapter as a workaround for the monitor, but I'd like the dock fixed when convenient.",
        "neutral"
    ),
    (
        "Need access to Epic reporting module",
        "Requesting access to Epic Reporting Workbench. I've been assigned to the new quality metrics project and need to pull patient outcome data. My role-based access currently only includes clinical modules.",
        "My director has submitted the Epic access request form. This ticket is for IT tracking.",
        "neutral"
    ),
    (
        "Scheduled maintenance question — will Epic be down?",
        "I saw an email about scheduled maintenance this Saturday. Will Epic Hyperspace be unavailable? If so, what hours? We need to plan paper-based downtime procedures for our unit.",
        "Just need confirmation of the timing so we can prepare. Thank you.",
        "neutral"
    ),
    (
        "Keyboard replacement needed",
        "The spacebar on my keyboard sticks intermittently. Some keypresses require extra force. Workstation at nursing station 5A, asset tag WS-5A-003. Standard USB keyboard.",
        "Not urgent — whenever a replacement is available.",
        "neutral"
    ),
    (
        "File recovery request from OneDrive",
        "I accidentally deleted a folder called 'Q1 Reports' from my OneDrive yesterday. I need it restored. The folder contained about 15 Excel files with budget data.",
        "I checked the OneDrive recycle bin but it's not there. It may have been auto-purged.",
        "neutral"
    ),
    (
        "Badge access request for new department area",
        "I transferred to Radiology and need badge access to the Radiology reading rooms (rooms 200-210, basement level). My current badge only works for general areas and my old Nursing unit.",
        "My new manager, Dr. Steven Wright, can confirm the transfer. Start date in Radiology was last Monday.",
        "neutral"
    ),
    (
        "Workstation relocation request",
        "Our department is rearranging offices. I need my desktop workstation moved from room 508 to room 512 (same floor, same wing). Both rooms have active network ports.",
        "We're planning the move for this Friday after 5 PM. Can IT assist with disconnecting and reconnecting?",
        "neutral"
    ),
    (
        "Patient portal inquiry — MyChart activation",
        "A patient is having trouble activating their MyChart account. They received the activation code but get an error when entering it. Patient MRN provided separately via secure channel.",
        "Patient is in the lobby now. If someone can walk me through troubleshooting, I can help them directly.",
        "neutral"
    ),
    (
        "Bluetooth headset pairing issue",
        "Cannot pair my Jabra Evolve2 headset with my laptop via Bluetooth. The headset pairs fine with my phone. Laptop Bluetooth is on and discovers the headset but fails during pairing.",
        "I use this for Teams calls. USB dongle works as a workaround but Bluetooth would be preferred.",
        "neutral"
    ),
    (
        "Guest WiFi access for visiting consultant",
        "We have an external consultant visiting our facility next week (April 21-25). They'll need guest WiFi access for their laptop to access their own company's VPN. Name: Dr. Karen Whitfield, Deloitte.",
        "Please provide the guest access credentials. I'll distribute them to the consultant upon arrival.",
        "neutral"
    ),
    (
        "Requesting shared mailbox for department",
        "The Cardiology Outpatient clinic needs a shared mailbox: cardiology.outpatient@trinityhealth.org. Access needed for 8 staff members. List of names attached. Manager approval from Dr. Chen attached.",
        "We'd like this set up within the next week if possible.",
        "neutral"
    ),
    (
        "Application error when generating reports in Epic",
        "When running the 'Daily Census' report in Epic Reporting Workbench, I get error code WDE-1042. The report worked fine last week. Other reports seem to generate normally.",
        "I can provide the full error log if needed. No rush — we have a manual workaround.",
        "neutral"
    ),
    (
        "USB ports not working on workstation",
        "None of the USB ports on my desktop workstation (Dell OptiPlex, asset WS-4N-012) are recognizing devices. Mouse and keyboard work (they're PS/2) but USB drives and peripherals are not detected.",
        "Tried front and rear USB ports. None respond. Device Manager shows the USB controllers.",
        "neutral"
    ),
    (
        "Requesting training environment access for Epic",
        "I'm attending Epic refresher training next week and need access to the Epic training environment (PLY). My trainer is Marcus Jenkins in Clinical Informatics. Training dates: April 21-23.",
        "My production Epic access is current — just need the training environment added.",
        "neutral"
    ),
    (
        "Scanner not feeding documents properly",
        "The document scanner at the HIM (Health Information Management) workstation is double-feeding pages and producing skewed images. Model: Fujitsu fi-7160, asset SCN-HIM-01.",
        "We scan patient records daily. This is our only scanner so we'd appreciate timely repair or replacement.",
        "neutral"
    ),
    (
        "Webcam not detected in Teams",
        "My built-in laptop webcam is not detected by Microsoft Teams. Camera works in the Windows Camera app but Teams shows 'No camera found.' I've reinstalled Teams and updated drivers.",
        "I have a patient telehealth visit at 3 PM so a fix before then would be appreciated.",
        "neutral"
    ),
    (
        "Archive old email to free up mailbox space",
        "My Outlook mailbox is at 98% capacity. I need to archive emails older than 2 years to free up space. I don't want to delete anything — just move to archive.",
        "Is this something IT can help with, or is there a self-service process?",
        "neutral"
    ),
    (
        "CPOE order entry slow during morning rounds",
        "Epic CPOE (Computerized Provider Order Entry) is noticeably slow between 7-9 AM during morning rounds. Order entry that normally takes seconds is taking 30-45 seconds. Afternoons seem fine.",
        "Multiple providers on our unit are experiencing this. Likely a peak-usage performance issue.",
        "neutral"
    ),
    (
        "Request to update name in systems after legal name change",
        "I've legally changed my name. Old name: Patricia Davis. New name: Patricia Davis-Monroe. HR has been updated. Requesting update across IT systems: AD, email, Epic user profile, badge.",
        "Legal documentation has been filed with HR. Please coordinate with them for verification.",
        "neutral"
    ),
    (
        "Workstation imaging request for 5 new PCs",
        "We received 5 new Dell OptiPlex desktops for the pharmacy department. They need to be imaged with the standard Trinity Health clinical workstation image and domain-joined.",
        "PCs are unboxed and in IT storage room B. Asset tags: WS-PH-101 through WS-PH-105.",
        "neutral"
    ),
    (
        "Power strip tripping circuit in server closet",
        "The power strip in the 3rd floor IDF closet trips its breaker when the UPS kicks in during power fluctuations. This has happened twice this month and takes down the floor's network switches temporarily.",
        "Facilities has looked at it and says the circuit is rated correctly. May need a different UPS or load balancing.",
        "neutral"
    ),
    (
        "Discharge summary template missing fields",
        "The discharge summary template in Epic is missing the 'Follow-up Appointments' section that was added last month. It appears on some workstations but not others.",
        "Might be a template version issue. We're using template ID DS-2026-03. Let me know if you need more details.",
        "neutral"
    ),

    # POSITIVE - grateful, complimentary, satisfied
    (
        "Thank you — laptop replacement was fast",
        "Received my replacement laptop today. Everything was set up perfectly — all my apps, printers, and Epic shortcuts were pre-configured. The migration from my old machine was seamless.",
        "Huge thank you to Alex Ramirez who handled this. He was professional, explained everything clearly, and even stayed late to make sure my docking station worked. Best IT experience I've had here. Please pass along my appreciation to his manager!",
        "positive"
    ),
    (
        "Compliment for service desk — quick resolution",
        "Called about an Epic access issue this morning and it was resolved within 20 minutes. The technician was knowledgeable, patient, and walked me through verifying everything worked before closing the call.",
        "I just want to say thank you. I know you all deal with frustrated people all day and I wanted to make sure positive feedback gets recorded too. Your team is doing a great job.",
        "positive"
    ),
    (
        "New conference room AV setup is excellent",
        "The new AV setup in the main conference room works beautifully. One-touch screen sharing, clear audio, and the camera tracking actually works. Our hybrid meetings are so much better now.",
        "This is a night and day improvement from what we had before. The implementation team did a fantastic job and the training session they held was very helpful. Well done!",
        "positive"
    ),
    (
        "Epic mobile app working great on new iPads",
        "The new iPad deployment with Epic Haiku/Canto is working excellently. Rounding is faster, and being able to enter orders at the bedside has improved our workflow significantly.",
        "I was skeptical when we heard about this rollout, but I'm a convert. The training was good, the devices are fast, and the nurses on my unit are all positive about it. Great project by IT.",
        "positive"
    ),
    (
        "Appreciation — after-hours support during system issue",
        "During last Saturday's network outage, the on-call IT team was responsive, communicative, and had systems restored faster than expected. Their regular status updates kept our staff informed and calm.",
        "Working a weekend shift during a system outage is stressful for everyone. The IT team handled it with professionalism and kept us updated every 30 minutes via email. Special thanks to Priya Sharma who coordinated everything. Excellent crisis management.",
        "positive"
    ),
    (
        "Self-service portal is much improved",
        "Just wanted to note that the redesigned IT self-service portal is much easier to use. I was able to reset my own password, request software, and check ticket status without calling anyone. Nice upgrade.",
        "I remember when the old portal was confusing and slow. This new version is clean, intuitive, and fast. Whatever team worked on this did a great job. Makes my life easier.",
        "positive"
    ),

    # MORE NEGATIVE
    (
        "Pharmacy system down — cannot verify medications",
        "The Pyxis MedStation on 6th floor is offline and showing 'Communication Error.' Nurses cannot pull scheduled medications. We're using paper backup but this is dangerous for a busy med-surg unit.",
        "This is the SECOND time this month. Patients have medications due NOW and we're doing manual verification which takes 3x as long and is more error-prone. Patient safety is at risk. Get someone here NOW.",
        "negative"
    ),
    (
        "Radiology images not loading — PACS issue",
        "PACS images are not loading in the Sectra viewer. Thumbnails appear but full images time out. This is affecting all radiologists in the reading room. We cannot read studies.",
        "We have 47 unread studies and climbing. ER is sending stat reads that we physically cannot look at. This is a clinical emergency, not a routine IT issue. We need immediate escalation to Sectra support.",
        "negative"
    ),
    (
        "Recurring issue STILL not fixed after 5 tickets",
        "This is my 5th ticket about the same issue — my Citrix session disconnects randomly throughout the day. Previous ticket numbers: INC0089234, INC0089567, INC0090012, INC0090445. Each time I'm told it's fixed, and each time it comes back.",
        "I have zero confidence this will be resolved. I've spent more time on the phone with IT than I have with patients this week. I want to speak with an IT manager about this. The insanity of repeating the same troubleshooting steps over and over needs to stop.",
        "negative"
    ),
    (
        "Cannot schedule appointments — system frozen",
        "The scheduling module in Epic is frozen for all users in our clinic. We cannot book, modify, or cancel patient appointments. Front desk staff are taking names on paper. This started at 8 AM.",
        "We have 200+ patients scheduled today across 12 providers and we can't manage any of it electronically. Patients are showing up and we can't confirm their appointments. This is chaos. Please help ASAP.",
        "negative"
    ),

    # MORE NEUTRAL
    (
        "Backup verification request",
        "Please verify that the nightly backup for the Cardiology department shared drive completed successfully last night. We're doing a quarterly audit and need confirmation.",
        "If you could send me the backup log or a confirmation email, that would be sufficient. Thank you.",
        "neutral"
    ),
    (
        "Meeting room booking system question",
        "Is there a way to book conference rooms through Outlook? I've been calling the front desk to reserve rooms and was told there might be an Outlook integration available.",
        "If there's a guide or documentation on how to set this up, that would be great.",
        "neutral"
    ),
    (
        "Old workstation ready for pickup",
        "I have my old Dell desktop ready for IT pickup following my laptop deployment last week. It's in room 440 with the old monitor, keyboard, and mouse. Asset tag: WS-4N-OLD-008.",
        "Please arrange pickup at your convenience. I've removed all personal files per the checklist.",
        "neutral"
    ),
    (
        "Query about software license availability",
        "Does Trinity Health have an enterprise license for Visio? I need it for creating process flow diagrams for our quality improvement project. If not, what's the request process?",
        "No rush on this. Just planning ahead for next month's project kickoff.",
        "neutral"
    ),
    (
        "Requesting static IP for medical device",
        "We're installing a new infusion pump system that requires a static IP address on the clinical VLAN. The device MAC address is AA:BB:CC:DD:EE:01. Location: ICU, Bed 12.",
        "Biomedical Engineering is coordinating the installation. Contact: Derek Owens. Target date: April 22.",
        "neutral"
    ),
    (
        "Annual PC refresh — department schedule inquiry",
        "When is the Laboratory department scheduled for the annual PC refresh? Several of our workstations are running slow and we want to know if replacement is coming soon or if we should request repairs.",
        "Our oldest machines are 2021 Dell OptiPlex 5090s. Let me know if we're on the schedule.",
        "neutral"
    ),
    (
        "Requesting after-hours access to server room",
        "I need after-hours badge access to Server Room A for scheduled maintenance this Saturday 4/19, approximately 6 AM to 10 AM. My manager (Tony Baxter) has approved.",
        "I'll have my Trinity Health badge and a valid change request number. Please advise the approval process.",
        "neutral"
    ),
    (
        "Print job stuck in queue",
        "I sent a print job to the 2nd floor admin printer about an hour ago and it's stuck in the queue. I can't cancel it from my workstation. Other print jobs from other users seem to be going through.",
        "Can you clear my stuck print job? The document name is 'Q1_Budget_Final.xlsx'. Thank you.",
        "neutral"
    ),
    (
        "Two-factor authentication setup help",
        "I got a new phone and need to re-register it with Duo for MFA. My old phone was wiped. I can come to the IT office with my badge and photo ID for identity verification.",
        "I can stop by anytime today. What's the process?",
        "neutral"
    ),
    (
        "Application compatibility question — Windows 11",
        "Our department uses a legacy clinical application called MedTrack v3.2. Before the Windows 11 migration, can you confirm it's been tested for compatibility? We rely on it for medication tracking.",
        "If it's not compatible, we need to know ASAP so we can plan a workaround or delay our migration.",
        "neutral"
    ),

    # MORE POSITIVE
    (
        "Quick fix — impressed with response time",
        "Called about an Outlook issue at 9:05 AM and it was fixed by 9:12 AM. Seven minutes. The tech knew exactly what the problem was and fixed it remotely without me having to do anything.",
        "That might be the fastest IT resolution I've ever experienced. Kudos to the team. I wish all problems were handled this efficiently!",
        "positive"
    ),
    (
        "Training session was very helpful",
        "Attended the Epic Hyperspace refresher training yesterday. The trainer was excellent — explained the new features clearly and gave us hands-on practice time. I learned several shortcuts I didn't know about.",
        "I actually enjoyed an IT training session, which is saying something! The materials were well-prepared and the trainer was engaging. Please schedule more of these for our department.",
        "positive"
    ),

    # ADDITIONAL NEGATIVE for variety
    (
        "On-call schedule not updating in system",
        "The on-call schedule in Amcom hasn't been updated for this week. Pages are going to last week's on-call physician who is now on vacation. Urgent consult pages are being missed.",
        "A covering physician had to be tracked down manually for an urgent consult because the page went to the wrong person. This needs to be fixed immediately before someone gets hurt.",
        "negative"
    ),
    (
        "Spam filter blocking legitimate patient emails",
        "Our department is not receiving emails from several referring physician offices. The emails are being quarantined by the spam filter. We've reported this twice before and the whitelist fix didn't stick.",
        "Patient referrals are getting lost in a spam filter. We've had patients show up for appointments we never received the referral for. This keeps happening and the fixes don't last. Very frustrating.",
        "negative"
    ),
    (
        "Blood bank system interface down",
        "The interface between Epic and the blood bank system (Softbank) is down. We cannot electronically verify blood products. Manual verification procedures are in place but this significantly slows transfusions.",
        "We have 3 patients waiting for blood products. Manual crossmatch verification takes 3x longer. Every minute counts for these patients. This interface has been unreliable for months and needs a permanent fix.",
        "negative"
    ),
    (
        "Remote desktop lagging badly for telehealth",
        "When conducting telehealth visits via Citrix remote desktop, there is a 3-5 second video/audio lag. Patients think their connection is bad but it's on our end. It makes clinical conversations very difficult.",
        "I had to end a telehealth visit early today because the lag made it impossible to have a meaningful clinical conversation. The patient was elderly and confused by the delays. This is affecting patient care quality.",
        "negative"
    ),

    # ADDITIONAL NEUTRAL
    (
        "Security certificate warning on internal site",
        "When accessing the internal HR portal (hr.trinityhealth.internal), Chrome shows a certificate warning. I can click through it but wanted to report it. The certificate appears to have expired April 12.",
        "Just reporting — I can still access the site by proceeding past the warning.",
        "neutral"
    ),
    (
        "Requesting ergonomic keyboard",
        "I'd like to request an ergonomic keyboard (Microsoft Sculpt or similar). I'm experiencing wrist discomfort from the standard keyboard. My manager has approved the purchase. Cost center: 44280.",
        "If there's a specific ergonomic equipment request process through Occupational Health, please let me know.",
        "neutral"
    ),
    (
        "Application timeout settings too short",
        "Epic auto-logs me out after 5 minutes of inactivity, but I frequently step away to attend to patients and lose my place in documentation. Can the timeout be extended to 15 minutes for clinical users?",
        "I understand security requirements but 5 minutes is impractical for bedside nursing. Tap-in/tap-out with Imprivata might be a better solution. What are the options?",
        "neutral"
    ),
    (
        "Mapping network drive on new workstation",
        "I need help mapping the L: drive (\\\\fileserver\\labshare) on my new workstation. I had it on my old machine but it didn't carry over during the migration.",
        "I know the path and have access — just need the drive letter mapped. Can you do this remotely?",
        "neutral"
    ),

    # ONE MORE POSITIVE
    (
        "Smooth go-live for new scheduling system",
        "Just wanted to acknowledge that the new scheduling system go-live this week was remarkably smooth. The preparation, communication, and support during the transition were excellent.",
        "I've been through many system go-lives at various hospitals and this was the best organized one I've experienced. The super-user support at every station made a huge difference. Whatever you did differently this time, keep doing it!",
        "positive"
    ),

    # --- BATCH 2: 16 more tickets to reach ~100 ---

    # NEGATIVE
    (
        "Dictation system dropping words mid-sentence",
        "Nuance Dragon Medical dictation is dropping words and inserting incorrect terms. 'Administer 10mg morphine' became 'administer morphine' — missing the dosage entirely. This is a clinical documentation risk.",
        "I've reported this three times. Medication dosages are being omitted from notes. If a nurse acts on an incomplete dictation, a patient could be harmed. I shouldn't have to proofread every single sentence for missing words. Fix this or give us a different product.",
        "negative"
    ),
    (
        "OR scheduling board blank — surgeries today",
        "The surgical scheduling display boards in the OR suite are showing blank screens. Staff cannot see the daily schedule, room assignments, or case status. We have 14 surgeries scheduled today.",
        "Surgeons are asking me where their cases are and I'm printing paper schedules like it's 1995. This board was installed 2 months ago and has gone down 4 times already. We paid a lot of money for something that doesn't work.",
        "negative"
    ),
    (
        "Patient data visible on unlocked workstation",
        "Found a shared workstation in the ER hallway logged into Epic with a patient record open. The auto-lock didn't engage. Anyone walking by could see PHI. This is a HIPAA violation waiting to happen.",
        "This is the third time I've found an unlocked workstation with patient data visible in a public area. Your auto-lock policy clearly isn't working. If a patient or family member sees this, we'll have a reportable breach. When is IT going to take this seriously?",
        "negative"
    ),
    (
        "Lab interface sending results to wrong patient chart",
        "A lab result was filed to the wrong patient's chart via the HL7 interface. We caught it during nursing review. The MRNs differ by one digit. Investigating whether this is a one-time error or systemic.",
        "If we hadn't caught this, a patient could have received treatment based on someone else's lab values. I need a full audit of recent lab result filings and I need it today. This is as serious as it gets.",
        "negative"
    ),
    (
        "Elevator emergency phone not connecting to dispatch",
        "Tested the emergency phone in Elevator 3 (main building) as part of our quarterly safety check. The phone does not connect — dead silence when picked up. This is a life safety issue.",
        "This is a Joint Commission compliance requirement. If someone is trapped in that elevator, they cannot call for help. I've reported this to Facilities too but the phone system is IT's responsibility. Needs immediate attention.",
        "negative"
    ),
    (
        "EHR timeout losing 30 minutes of documentation",
        "Epic timed out while I was documenting a complex patient assessment. I lost approximately 30 minutes of detailed clinical notes. The auto-save did not preserve my work. I had to re-document everything from memory.",
        "This is demoralizing. I spent my lunch break re-typing notes. Auto-save is supposed to prevent this but it clearly doesn't work. Nurses are already short on time — losing documentation to timeouts is unacceptable. PLEASE fix the auto-save.",
        "negative"
    ),

    # NEUTRAL
    (
        "Requesting second monitor for billing workstation",
        "Requesting a second 24-inch monitor for my workstation in Revenue Cycle, room 220. Dual monitors are standard for billing staff per department policy. Manager approval: attached.",
        "Current setup only has one monitor. The other billing specialists all have two. Please advise on timeline.",
        "neutral"
    ),
    (
        "Conference call bridge number not working",
        "The department conference bridge number (x8800) plays a busy signal when dialed internally. External callers report it rings but nobody picks up. We use this for daily 8 AM huddles.",
        "We've been using a personal Teams meeting as a workaround. Not urgent if the fix is coming soon, but we'd like the bridge restored.",
        "neutral"
    ),
    (
        "Requesting mobile device for rounding physician",
        "Dr. Laura Nguyen needs an iPad Pro with Epic Haiku configured for inpatient rounding. She's a new hospitalist starting May 1. Manager: Dr. Robert Chen. Cost center: 44350.",
        "Standard hospitalist mobile device package. Please coordinate with Dr. Nguyen directly for pickup and training scheduling.",
        "neutral"
    ),
    (
        "Inventory scan guns not syncing",
        "Three Zebra handheld scanners in the Supply Chain warehouse are not syncing their scans to the inventory management system. The scanners capture barcodes locally but the data doesn't upload.",
        "We're recording scans on paper as a backup. Asset tags: SCN-SC-04, SCN-SC-05, SCN-SC-07. Please check the wireless sync settings.",
        "neutral"
    ),
    (
        "Request to disable former employee account",
        "Employee Mark Sullivan (ID: 4459923) transferred to another health system as of April 14. Please disable his AD account, email, Epic access, VPN, and badge. HR separation notice attached.",
        "Standard offboarding. Please confirm when all access has been revoked.",
        "neutral"
    ),
    (
        "Requesting firewall rule for vendor remote access",
        "Our Epic support vendor (Vendor: Apex Health IT) needs remote access for a scheduled optimization session on April 22. They need access to the Epic Clarity reporting server from IP range 203.0.113.0/24.",
        "Change request CR-2026-0442 has been approved. Access should be time-limited to April 22, 8 AM - 5 PM ET.",
        "neutral"
    ),
    (
        "Nurse call system integration question",
        "We're evaluating whether the nurse call system (Hill-Rom) can be integrated with Epic to auto-document response times. Is this technically feasible with our current infrastructure?",
        "This is exploratory — no action needed yet. Just looking for a technical assessment before we bring it to the steering committee.",
        "neutral"
    ),
    (
        "Requesting access to data warehouse for analytics",
        "I need read-only access to the Epic Caboodle data warehouse for a population health analytics project. My director (Dr. Emily Foster) has approved. I have completed the data governance training.",
        "I'll primarily need access to the encounter and diagnosis tables. Happy to schedule a call to discuss scope if needed.",
        "neutral"
    ),

    # POSITIVE
    (
        "Desktop support went above and beyond",
        "Had a major issue with my workstation the day before a Joint Commission survey. Derek Owens from Desktop Support came within 15 minutes, identified a failing hard drive, and had me on a loaner within an hour.",
        "Derek saved us from a potentially embarrassing situation during our survey. He was calm, efficient, and even followed up the next day to make sure everything was still working. This is the kind of IT support that makes a real difference. Please recognize him.",
        "positive"
    ),
    (
        "New VPN solution is rock solid",
        "Since the VPN upgrade last month, I haven't had a single dropped connection while working from home. Previously I was reconnecting 5-6 times per day. Whatever changes were made to the infrastructure worked perfectly.",
        "I just want to give credit where it's due. The remote work experience has gone from frustrating to seamless. Several of my colleagues have said the same thing. Thank you to whoever led this project.",
        "positive"
    ),
]


def random_datetime(start, end):
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)


def generate_tickets():
    rows = []
    base_inc = 91000
    start_date = datetime(2026, 1, 6)
    end_date = datetime(2026, 4, 17)

    for i, template in enumerate(TICKET_TEMPLATES):
        short_desc, description, customer_comment, sentiment = template
        inc_number = f"INC00{base_inc + i}"

        opened_dt = random_datetime(start_date, end_date)
        category = random.choice(list(CATEGORIES.keys()))
        subcategory = random.choice(CATEGORIES[category])
        caller = random.choice(CALLERS)
        contact_type = random.choice(CONTACT_TYPES)
        location = random.choice(LOCATIONS)
        business_service = random.choice(BUSINESS_SERVICES)
        assignment_group = random.choice(ASSIGNMENT_GROUPS)
        assigned_to = random.choice(TECHNICIANS)

        ci_category = category if category in CONFIGURATION_ITEMS else random.choice(list(CONFIGURATION_ITEMS.keys()))
        config_item = random.choice(CONFIGURATION_ITEMS[ci_category])

        # Priority/impact/urgency - negative tickets trend higher priority
        if sentiment == "negative":
            priority = random.choice(["1 - Critical", "1 - Critical", "2 - High", "2 - High", "3 - Moderate"])
            impact = random.choice(["1 - High", "1 - High", "2 - Medium"])
            urgency = random.choice(["1 - High", "1 - High", "2 - Medium"])
        elif sentiment == "positive":
            priority = random.choice(["3 - Moderate", "4 - Low"])
            impact = random.choice(["2 - Medium", "3 - Low"])
            urgency = random.choice(["2 - Medium", "3 - Low"])
        else:
            priority = random.choice(PRIORITIES)
            impact = random.choice(IMPACTS)
            urgency = random.choice(URGENCIES)

        # State - most tickets resolved/closed, some open
        if i < 10:
            state = random.choice(["New", "In Progress", "In Progress", "On Hold"])
            resolved_dt = ""
            closed_dt = ""
            resolution_code = ""
            resolution_notes = ""
        elif sentiment == "positive":
            state = "Closed"
            resolved_dt = opened_dt + timedelta(hours=random.randint(1, 48))
            closed_dt = resolved_dt + timedelta(hours=random.randint(1, 24))
            resolution_code = "Solved (Permanently)"
            resolution_notes = "Issue resolved. Positive feedback noted."
        else:
            state = random.choice(["Resolved", "Resolved", "Closed", "Closed", "Closed", "In Progress"])
            if state in ("Resolved", "Closed"):
                resolved_dt = opened_dt + timedelta(hours=random.randint(1, 96))
                closed_dt = resolved_dt + timedelta(hours=random.randint(1, 48)) if state == "Closed" else ""
                resolution_code = random.choice(RESOLUTION_CODES[:3])
                if resolution_code == "Solved (Permanently)":
                    resolution_notes = random.choice([
                        "Root cause identified and permanent fix applied.",
                        "Replaced faulty hardware component. Tested and verified working.",
                        "Configuration corrected. User confirmed issue resolved.",
                        "Software updated to latest version. Issue no longer reproducible.",
                        "Access provisioned per approved request. User confirmed working.",
                        "Network port activated and tested. Connectivity confirmed.",
                        "Account unlocked and cached credentials cleared across all devices.",
                        "Printer driver reinstalled and test page printed successfully.",
                    ])
                elif resolution_code == "Solved (Workaround)":
                    resolution_notes = random.choice([
                        "Temporary workaround provided. Permanent fix scheduled for next maintenance window.",
                        "User provided alternate workflow. Root cause under investigation.",
                        "Rebooted system which resolved symptoms. Monitoring for recurrence.",
                        "Switched to backup system. Primary system escalated to vendor.",
                    ])
                else:
                    resolution_notes = random.choice([
                        "Unable to reproduce issue. User will reopen if it recurs.",
                        "Issue appears intermittent. Monitoring. Will escalate to vendor if it continues.",
                    ])
            else:
                resolved_dt = ""
                closed_dt = ""
                resolution_code = ""
                resolution_notes = ""

        sla_hours = {"1 - Critical": 4, "2 - High": 8, "3 - Moderate": 24, "4 - Low": 72}
        sla_due = opened_dt + timedelta(hours=sla_hours[priority])

        work_notes = random.choice([
            f"Assigned to {assigned_to}. Initial assessment in progress.",
            f"Contacted user for additional details. Awaiting response.",
            f"Escalated to {assignment_group} for further investigation.",
            f"Remote session established. Troubleshooting in progress.",
            f"Checked system logs — no errors found. Scheduling on-site visit.",
            f"Vendor ticket opened. Reference: VND-{random.randint(100000, 999999)}.",
            f"Applied patch KB{random.randint(1000000, 9999999)}. Monitoring.",
            f"User profile rebuilt. Testing in progress.",
            f"Hardware replacement ordered. ETA 2-3 business days.",
            f"Configuration change applied. Requested user verification.",
        ])

        rows.append({
            "Number": inc_number,
            "Opened": opened_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "Short Description": short_desc,
            "Description": description,
            "Caller": caller,
            "Contact Type": contact_type,
            "Category": category,
            "Subcategory": subcategory,
            "Priority": priority,
            "Impact": impact,
            "Urgency": urgency,
            "State": state,
            "Assignment Group": assignment_group,
            "Assigned To": assigned_to,
            "Configuration Item": config_item,
            "Location": location,
            "Business Service": business_service,
            "SLA Due": sla_due.strftime("%Y-%m-%d %H:%M:%S"),
            "Resolved": resolved_dt.strftime("%Y-%m-%d %H:%M:%S") if resolved_dt else "",
            "Closed": closed_dt.strftime("%Y-%m-%d %H:%M:%S") if closed_dt else "",
            "Resolution Code": resolution_code,
            "Resolution Notes": resolution_notes,
            "Customer Comments": customer_comment,
            "Work Notes": work_notes,
        })

    # Shuffle to mix sentiments naturally
    random.shuffle(rows)
    return rows


def main():
    rows = generate_tickets()
    fieldnames = [
        "Number", "Opened", "Short Description", "Description", "Caller",
        "Contact Type", "Category", "Subcategory", "Priority", "Impact",
        "Urgency", "State", "Assignment Group", "Assigned To",
        "Configuration Item", "Location", "Business Service", "SLA Due",
        "Resolved", "Closed", "Resolution Code", "Resolution Notes",
        "Customer Comments", "Work Notes",
    ]

    output_path = "trinity_health_service_tickets.csv"
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # Print summary
    sentiments = {}
    for t in TICKET_TEMPLATES:
        s = t[3]
        sentiments[s] = sentiments.get(s, 0) + 1
    print(f"Generated {len(rows)} tickets to {output_path}")
    print(f"Sentiment distribution: {sentiments}")


if __name__ == "__main__":
    main()

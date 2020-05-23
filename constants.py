VIALINK_DISASTER_KEY = "VL_DISASTER"
VIALINK_CALLS_KEY = "VL_CALLS"
TWO32_HELP_CALLS_KEY = "TWO32_HELP_CALLS"

VIALINK_NEEDS_COLUMNS = [
    "Concerns/Needs  - Disaster Services ",
    "Concerns/Needs  - Domestic Abuse/IPV",
    "Concerns/Needs  - Early Childhood Education ",
    "Concerns/Needs  - Education/ Employment ",
    "Concerns/Needs  - Environmental Quality & Prtcn ",
    "Concerns/Needs  - Health Care ",
    "Concerns/Needs  - Interpersonal",
    "Concerns/Needs  - Mental Health",
    "Concerns/Needs  - Mental Health Concerns",
    "Concerns/Needs  - Organizational Development",
    "Concerns/Needs  - Other ",
    "Concerns/Needs  - Other Community Services",
    "Concerns/Needs  - Protective Service/Abuse",
    "Concerns/Needs  - Public Asst & Social Insurance",
    "Concerns/Needs  - Relationship Concerns / Issues ",
    "Concerns/Needs  - Self-Harm",
    "Concerns/Needs  - Sexuality",
]

VIALINK_REQUIRED_COLUMNS_CALLS = [
    "CallReportNum",
    "ReportVersion",
    "CallDateAndTimeStart",
    "CityName",
    "CountyName",
    "StateProvince",
    "PostalCode",
    "Call Information - Program",
    "Demographics - Age",
    "Demographics - Gender",
] + VIALINK_NEEDS_COLUMNS

VIALINK_REQUIRED_COLUMNS_DISASTER = [
    "CallReportNum",
    "ReportVersion",
    "CallDateAndTimeStart",
    "CityName",
    "CountyName",
    "StateProvince",
    "PostalCode",
    "Client Information - Age Group",
    "Client Information - Call Type",
    "Client Information - Identifies as",
    "Concerns/Needs - Concerns/Needs",
    "Contact Source - Program ",  # ending space is needed
    "Needs - Basic Needs Requested",
]

TWO32_HELP_REQUIRED_COLUMNS = [
    "CallReportNum",
    "ReportVersion",
    "CallDateAndTimeStart",
    "CityName",
    "CountyName",
    "StateProvince",
    "PostalCode",
    "Client Information - Date of Birth",
    "Client Information - Call Type",
    "Call Outcome - What concerns/needs were identified?",
    "Client Information - Identifies as",
    "Needs - Basic Needs Requested",
]

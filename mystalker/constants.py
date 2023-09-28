
import http
import socket
from typing import List
from typing import Tuple

import requests.exceptions
import urllib3.exceptions

# Default values
DEFAULT_DATABASE_RENEW_INTERVAL: int = 7
DEFAULT_LOOP_DIGIT_START: int = 0
DEFAULT_LOOP_DIGIT_STOP: int = 10000
DEFAULT_LOOP_BIRTH_DATE_START: str = "010101"
DEFAULT_LOOP_BIRTH_DATE_STOP: str = "210101"

# Constants
APP_AUTHOR: str = "Kim"
APP_NAME: str = "MyStalker"

CHECKPOINT_FILENAME: str = "mystalker.checkpoint"
SCHOOLS_FILENAME: str = "schools.csv"
STUDENTS_FILENAME: str = "students.csv"

DATABASE_FILE_URL: str = "https://raw.githubusercontent.com/LynBean/MyStalker/main/database.csv"
GITHUB_URL: str = "https://github.com/LynBean/MyStalker"

BASE_URL: str = "https://sapsnkra.moe.gov.my/"
IBUBAPA_MAIN_URL: str = BASE_URL + "ibubapa2/indexv2.php"
IBUBAPA_SEMAK_URL: str = BASE_URL + "ibubapa2/semak.php"
PAPAR_CARIAN_PELAJAR_URL: str = BASE_URL + "ajax/papar_carianpelajar.php"
PAPAR_CARIAN_URL: str = BASE_URL + "ajax/papar_carian.php"
SENARAI_PPD_URL: str = BASE_URL + "ajax/senarai_ppd.php"
SENARAI_SEKOLAH_URL: str = BASE_URL + "ajax/ddl_senarai_sekolah.php"

USER_AGENT: dict = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
}

NETWORK_ERROR_EXCEPTIONS: tuple = (
    ConnectionRefusedError,
    http.client.BadStatusLine,
    http.client.CannotSendHeader,
    http.client.CannotSendRequest,
    http.client.HTTPException,
    http.client.ImproperConnectionState,
    http.client.IncompleteRead,
    http.client.InvalidURL,
    http.client.LineTooLong,
    http.client.LineTooLong,
    http.client.NotConnected,
    http.client.RemoteDisconnected,
    http.client.ResponseNotReady,
    http.client.UnimplementedFileMode,
    http.client.UnimplementedFileMode,
    http.client.UnknownProtocol,
    http.client.UnknownTransferEncoding,
    requests.exceptions.ChunkedEncodingError,
    requests.exceptions.ConnectionError,
    requests.exceptions.ConnectTimeout,
    requests.exceptions.ContentDecodingError,
    requests.exceptions.FileModeWarning,
    requests.exceptions.HTTPError,
    requests.exceptions.InvalidHeader,
    requests.exceptions.InvalidJSONError,
    requests.exceptions.InvalidProxyURL,
    requests.exceptions.InvalidSchema,
    requests.exceptions.InvalidURL,
    requests.exceptions.JSONDecodeError,
    requests.exceptions.MissingSchema,
    requests.exceptions.ProxyError,
    requests.exceptions.ReadTimeout,
    requests.exceptions.RequestException,
    requests.exceptions.RequestsDependencyWarning,
    requests.exceptions.RequestsWarning,
    requests.exceptions.RetryError,
    requests.exceptions.SSLError,
    requests.exceptions.StreamConsumedError,
    requests.exceptions.Timeout,
    requests.exceptions.TooManyRedirects,
    requests.exceptions.UnrewindableBodyError,
    requests.exceptions.URLRequired,
    socket.gaierror,
    TimeoutError,
    urllib3.exceptions.BodyNotHttplibCompatible,
    urllib3.exceptions.ClosedPoolError,
    urllib3.exceptions.ConnectTimeoutError,
    urllib3.exceptions.DecodeError,
    urllib3.exceptions.DependencyWarning,
    urllib3.exceptions.EmptyPoolError,
    # urllib3.exceptions.FullPoolError,
    urllib3.exceptions.HeaderParsingError,
    urllib3.exceptions.HostChangedError,
    urllib3.exceptions.HTTPError,
    urllib3.exceptions.HTTPWarning,
    urllib3.exceptions.IncompleteRead,
    urllib3.exceptions.InsecurePlatformWarning,
    urllib3.exceptions.InsecureRequestWarning,
    urllib3.exceptions.InvalidChunkLength,
    urllib3.exceptions.InvalidHeader,
    urllib3.exceptions.LocationParseError,
    urllib3.exceptions.LocationValueError,
    urllib3.exceptions.MaxRetryError,
    # urllib3.exceptions.NameResolutionError,
    urllib3.exceptions.NewConnectionError,
    urllib3.exceptions.PoolError,
    urllib3.exceptions.ProtocolError,
    urllib3.exceptions.ProxyError,
    urllib3.exceptions.ProxySchemeUnknown,
    urllib3.exceptions.ProxySchemeUnsupported,
    urllib3.exceptions.ReadTimeoutError,
    urllib3.exceptions.RequestError,
    urllib3.exceptions.ResponseError,
    urllib3.exceptions.ResponseNotChunked,
    urllib3.exceptions.SecurityWarning,
    urllib3.exceptions.SSLError,
    urllib3.exceptions.SystemTimeWarning,
    urllib3.exceptions.TimeoutError,
    urllib3.exceptions.TimeoutStateError,
    urllib3.exceptions.UnrewindableBodyError,
    urllib3.exceptions.URLSchemeUnknown
)

### https://en.wikipedia.org/wiki/Malaysian_identity_card
PLACE_OF_BIRTH: List[Tuple[int, str]] = [
    (0, None),
    (1, "JOHOR"),
    (2, "KEDAH"),
    (3, "KELANTAN"),
    (4, "MELAKA"),
    (5, "NEGERI SEMBILAN"),
    (6, "PAHANG"),
    (7, "PENANG"),
    (8, "PERAK"),
    (9, "PERLIS"),
    (10, "SELANGOR"),
    (11, "TERENGGANU"),
    (12, "SABAH"),
    (13, "SARAWAK"),
    (14, "KUALA LUMPUR"),
    (15, "LABUAN"),
    (16, "PUTRAJAYA"),
    (17, None),
    (18, None),
    (19, None),
    (20, None),
    (21, "JOHOR"),
    (22, "JOHOR"),
    (23, "JOHOR"),
    (24, "JOHOR"),
    (25, "KEDAH"),
    (26, "KEDAH"),
    (27, "KEDAH"),
    (28, "KELANTAN"),
    (29, "KELANTAN"),
    (30, "MELAKA"),
    (31, "NEGERI SEMBILAN"),
    (32, "PAHANG"),
    (33, "PAHANG"),
    (34, "PENANG"),
    (35, "PENANG"),
    (36, "PERAK"),
    (37, "PERAK"),
    (38, "PERAK"),
    (39, "PERAK"),
    (40, "PERLIS"),
    (41, "SELANGOR"),
    (42, "SELANGOR"),
    (43, "SELANGOR"),
    (44, "SELANGOR"),
    (45, "TERENGGANU"),
    (46, "TERENGGANU"),
    (47, "SABAH"),
    (48, "SABAH"),
    (49, "SABAH"),
    (50, "SARAWAK"),
    (51, "SARAWAK"),
    (52, "SARAWAK"),
    (53, "SARAWAK"),
    (54, "KUALA LUMPUR"),
    (55, "KUALA LUMPUR"),
    (56, "KUALA LUMPUR"),
    (57, "KUALA LUMPUR"),
    (58, "LABUAN"),
    (59, "NEGERI SEMBILAN"),
    (60, "BRUNEI"),
    (61, "INDONESIA"),
    (62, "CAMBODIA"),
    (63, "LAOS"),
    (64, "MYANMAR"),
    (65, "PHILIPPINES"),
    (66, "SINGAPORE"),
    (67, "THAILAND"),
    (68, "VIETNAM"),
    (69, None),
    (70, None),
    (71, "A PERSON BORN OUTSIDE MALAYSIA PRIOR TO 2001. EXCLUDING THOSE BORN ABROAD WITHOUT HOLDING HIGH QUALITY IDENTITY CARD"),
    (72, "A PERSON BORN OUTSIDE MALAYSIA PRIOR TO 2001. EXCLUDING THOSE BORN ABROAD WITHOUT HOLDING HIGH QUALITY IDENTITY CARD"),
    (73, None),
    (74, "CHINA"),
    (75, "INDIA"),
    (76, "PAKISTAN"),
    (77, "SAUDI ARABIA"),
    (78, "SRI LANKA"),
    (79, "BANGLADESH"),
    (80, None),
    (81, None),
    (82, "UNKNOWN-STATE"),
    (83, "ASIA-PACIFIC: AMERICAN SAMOA / AUSTRALIA / CHRISTMAS ISLAND / COCOS (KEELING) ISLANDS / COOK ISLANDS / FIJI / FRENCH POLYNESIA / GUAM / HEARD ISLAND AND MCDONALD ISLANDS / MARSHALL ISLANDS / MICRONESIA / NEW CALEDONIA / NEW ZEALAND / NIUE / NORFOLK ISLAND / PAPUA NEW GUINEA / TIMOR LESTE / TOKELAU / UNITED STATES MINOR OUTLYING ISLANDS / WALLIS AND FUTUNA ISLANDS"),
    (84, "SOUTH AMERICA: ANGUILLA / ARGENTINA / ARUBA / BOLIVIA / BRAZIL / CHILE / COLOMBIA / ECUADOR / FRENCH GUINEA / GUADELOUPE / GUYANA / PARAGUAY / PERU / SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS / SURINAME / URUGUAY / VENEZUELA"),
    (85, "AFRICA: ALGERIA / ANGOLA / BOTSWANA / BURUNDI / CAMEROON / CENTRAL AFRICAN REPUBLIC / CHAD / CONGO-BRAZZAVILLE / CONGO-KINSHASA / DJIBOUTI / EGYPT / ERITREA / ETHIOPIA / GABON / GAMBIA / GHANA / GUINEA / KENYA / LIBERIA / MALAWI / MALI / MAURITANIA / MAYOTTE / MOROCCO / MOZAMBIQUE / NAMIBIA / NIGER / NIGERIA / RWANDA / RÉUNION / SENEGAL / SIERRA LEONE / SOMALIA / SOUTH AFRICA / SUDAN / SWAZILAND / TANZANIA / TOGO / TONGA / TUNISIA / UGANDA / WESTERN SAHARA / ZAIRE / ZAMBIA / ZIMBABWE"),
    (86, "EUROPE: ARMENIA / AUSTRIA / BELGIUM / CYPRUS / DENMARK / FAROE ISLANDS / FRANCE / FINLAND / FINLAND, METROPOLITAN / GERMANY / GERMANY, DEMOCRATIC REPUBLIC / GERMANY, FEDERAL REPUBLIC / GREECE / HOLY SEE (VATICAN CITY) / ITALY / LUXEMBOURG / MALTA / MEDITERRANEAN / MONACO / NETHERLANDS / NORTH MACEDONIA / NORWAY / PORTUGAL / REPUBLIC OF MOLDOVA / SLOVAKIA / SLOVENIA / SPAIN / SWEDEN / SWITZERLAND / UNITED KINGDOM-DEPENDENT TERRITORIES / UNITED KINGDOM-NATIONAL OVERSEAS / UNITED KINGDOM-OVERSEAS CITIZEN / UNITED KINGDOM-PROTECTED PERSON / UNITED KINGDOM-SUBJECT"),
    (87, "BRITAIN / GREAT BRITAIN / IRELAND"),
    (88, "MIDDLE EAST: BAHRAIN / IRAN / IRAQ / PALESTINE / JORDAN / KUWAIT / LEBANON / OMAN / QATAR / REPUBLIC OF YEMEN / SYRIA / TURKEY / UNITED ARAB EMIRATES / YEMEN ARAB REPUBLIC / YEMEN PEOPLE'S DEMOCRATIC REPUBLIC / ISRAEL"),
    (89, "FAR EAST: JAPAN / NORTH KOREA / SOUTH KOREA / TAIWAN"),
    (90, "CARIBBEAN: BAHAMAS / BARBADOS / BELIZE / COSTA RICA / CUBA / DOMINICA / DOMINICAN REPUBLIC / EL SALVADOR / GRENADA / GUATEMALA / HAITI / HONDURAS / JAMAICA / MARTINIQUE / MEXICO / NICARAGUA / PANAMA / PUERTO RICO / SAINT KITTS AND NEVIS / SAINT LUCIA / SAINT VINCENT AND THE GRENADINES / TRINIDAD AND TOBAGO / TURKS AND CAICOS ISLANDS / VIRGIN ISLANDS (USA)"),
    (91, "NORTH AMERICA: CANADA / GREENLAND / NETHERLANDS ANTILLES / SAINT PIERRE AND MIQUELON / UNITED STATES OF AMERICA"),
    (92, "SOVIET UNION / USSR: ALBANIA / BELARUS / BOSNIA AND HERZEGOVINA / BULGARIA / BYELORUSSIA / CROATIA / CZECH REPUBLIC / CZECHOSLOVAKIA / ESTONIA / GEORGIA / HUNGARY / LATVIA / LITHUANIA / MONTENEGRO / POLAND / REPUBLIC OF KOSOVO / ROMANIA / RUSSIAN FEDERATION / SERBIA / UKRAINE"),
    (93, "AFGHANISTAN / ANDORRA / ANTARCTICA / ANTIGUA AND BARBUDA / AZERBAIJAN / BENIN / BERMUDA / BHUTAN / BORA BORA / BOUVET ISLAND / BRITISH INDIAN OCEAN TERRITORY / BURKINA FASO / CAPE VERDE / CAYMAN ISLANDS / COMOROS / DAHOMEY / EQUATORIAL GUINEA / FALKLAND ISLANDS / FRENCH SOUTHERN TERRITORIES / GIBRALTAR / GUINEA-BISSAU / HONG KONG / ICELAND / IVORY COAST / KAZAKHSTAN / KIRIBATI / KYRGYZSTAN / LESOTHO / LIBYA / LIECHTENSTEIN / MACAU / MADAGASCAR / MAGHRIBI / MALAGASY / MALDIVES / MAURITIUS / MONGOLIA / MONTSERRAT / NAURU / NEPAL / NORTHERN MARIANAS ISLANDS / OUTER MONGOLIA / PALAU / PALESTINE / PITCAIRN ISLANDS / SAINT HELENA / SAINT LUCIA / SAINT VINCENT AND THE GRENADINES / SAMOA / SAN MARINO / SÃO TOMÉ AND PRÍNCIPE / SEYCHELLES / SOLOMON ISLANDS / SVALBARD AND JAN MAYEN ISLANDS / TAJIKISTAN / TURKMENISTAN / TUVALU / UPPER VOLTA / UZBEKISTAN / VANUATU / VATICAN CITY / VIRGIN ISLANDS (BRITISH) / WESTERN SAMOA / YUGOSLAVIA"),
    (94, None),
    (95, None),
    (96, None),
    (97, None),
    (98, "STATELESS / STATELESS PERSON ARTICLE 1/1954"),
    (99, "MECCA / NEUTRAL ZONE / NO INFORMATION / REFUGEE / REFUGEE ARTICLE 1/1951 / UNITED NATIONS SPECIALIZED AGENCY / UNITED NATIONS ORGANIZATION / UNSPECIFIED NATIONALITY")
]

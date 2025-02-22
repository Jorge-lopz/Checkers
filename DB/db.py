# --------------------------------------------------------------------------- #
#                                                                             #
#     db.py                                               +#######+           #
#                                                       +###########+         #
#     PROJECT: Checkers                       ·''''''''·#############         #
#     AUTHOR(S): Jorge                       '''''''''''+###########+         #
#                                            '''''''''''' +#######+           #
#     CREATED DATE: 17/01/2025               ''''''''''''                     #
#     LAST UPDATE: 18/01/2025                 `''''''''´                      #
#                                                                             #
# --------------------------------------------------------------------------- #

from supabase import create_client, Client  # Required package to easily connect to Supabase
import DB.schema as sch  # Database schema for the project

url: str =                                                                                                                                                              "https://cldyxcdaelouqxjnkolv.supabase.co"
key: str =                                                                                                                                                              "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNsZHl4Y2RhZWxvdXF4am5rb2x2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzcxMDU4NTgsImV4cCI6MjA1MjY4MTg1OH0._Po6_22wRsIdpa17dotqLia4uOLxE8v7sgDaaeD0TWw"

db: Client = create_client(url, key)

def getOpenings() -> list:
    """
    Called automatically when the game starts to retrieve all the predefined openings.
    :return: A list of all the openings stored on the database.
    """
    return [item[sch.OPENINGS_TRACE] for item in db.table(sch.TABLE_OPENINGS).select(sch.OPENINGS_TRACE).execute().data]

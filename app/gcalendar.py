from __future__ import print_function
from google_auth_oauthlib.flow import InstalledAppFlow
import datetime
# 구글 캘린더 API 서비스 객체 생성
import os.path
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

def gcalendarFirstSignin(name):
    print("first signin")
    # 구글 클라우드 콘솔에서 다운받은 OAuth 2.0 클라이언트 파일경로
    creds_filename = 'app/credit.json'
    # 사용 권한 지정
    # https://www.googleapis.com/auth/calendar	               캘린더 읽기/쓰기 권한
    # https://www.googleapis.com/auth/calendar.readonly	       캘린더 읽기 권한
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    # 파일에 담긴 인증 정보로 구글 서버에 인증하기
    # 새 창이 열리면서 구글 로그인 및 정보 제공 동의 후 최종 인증이 완료됩니다.
    flow = InstalledAppFlow.from_client_secrets_file(creds_filename, SCOPES)
    creds = flow.run_local_server(port=8080)

    with open('gcalendar_tokens/'+name+'_token.json', 'w') as token:
        token.write(creds.to_json())

    return get_calendar(creds)

def showgcalendar(name):
    print("show calendar")
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None

    if os.path.exists('gcalendar_tokens/' + name + '_token.json'):
        # while signed in
        creds = Credentials.from_authorized_user_file('gcalendar_tokens/' + name + '_token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # when access token expired
            creds.refresh(Request())
        else:
            # first sign in
            context = {'gcalendar_first_signin': 1}
            return context

        with open('gcalendar_tokens/' + name + '_token.json', 'w') as token:
            token.write(creds.to_json())

    return get_calendar(creds)

def get_calendar(creds):
    print("get calendar")
    service = build('calendar', 'v3', credentials=creds)
    today = datetime.date.today().isoformat()


    calendar_id = 'primary'
    today = datetime.date.today().isoformat()
    time_min = today + 'T00:00:00+09:00'
    time_max = today + 'T23:59:59+09:00'
    max_results = 5
    is_single_events = True
    orderby = 'startTime'

    events_result = service.events().list(calendarId=calendar_id,
                                          timeMin=time_min,
                                          timeMax=time_max,
                                          maxResults=max_results,
                                          singleEvents=is_single_events,
                                          orderBy=orderby
                                          ).execute()
    # print(events_result)
    # 구글 캘린더 일정 가져오기
    items = events_result.get('items')
    # 구글 캘린더 일정을 하나씩 확인
    gsummary = []
    gaddress = []
    gstart = []
    gend = []

    for item in items:
        # 일정 제목
        summary = item.get('summary')
        gsummary.append(summary)

        address = item.get('location')
        gaddress.append(address)

        start = item.get('start')
        gstart.append(start)

        end = item.get('end')
        gend.append(end)

    for summary in gsummary:
        print(summary)

    context= {
        'gsummary': gsummary,
        'gaddress': gaddress,
        'gstart': gstart,
        'gend': gend
    }


    return context

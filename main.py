import flet as ft

from services.club_service import ClubService
from services.match_service import MatchService
from services.pub_service import PubService

club_service = ClubService()
match_service = MatchService()
pub_service = PubService()


def main(page: ft.Page):

    page.title = "⚽ 해외축구 시청 가이드"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = "auto"

    # =====================
    # 입력 필드
    # =====================
    pub_id_field      = ft.TextField(label="펍 ID (수정/삭제용)")
    pub_name_field    = ft.TextField(label="펍 이름")
    address_field     = ft.TextField(label="주소")
    league_field      = ft.TextField(label="주요 리그")
    support_field     = ft.TextField(label="응원 구단 ID (1~20)")
    image_field       = ft.TextField(label="이미지 경로")
    club_search_field = ft.TextField(label="구단 이름 검색", expand=True)
    match_dropdown    = ft.Dropdown(label="추천받을 경기", expand=True)

    # =====================
    # 컨텐츠 영역
    # =====================
    content_area = ft.Column(scroll="auto", expand=True, spacing=12)
    title_text   = ft.Text("⚽ 축구 구단 목록", size=20, weight="bold")

    # =====================
    # 구단 카드 생성
    # =====================
    def make_club_card(club):
        return ft.Card(
            elevation=4,
            content=ft.Container(
                padding=14,
                width=180,
                content=ft.Column(
                    horizontal_alignment="center",
                    spacing=8,
                    controls=[
                        ft.Image(
                            src=club["logo_path"],
                            width=60, height=60,
                        ),
                        ft.Text(club["team_name"], size=15, weight="bold",
                                text_align="center"),
                        ft.Text(club["league"], size=12, text_align="center"),
                        ft.Text(club["manager"], size=12, text_align="center"),
                    ]
                )
            )
        )

    # =====================
    # 구단 조회 (2열 wrap)
    # =====================
    def show_clubs(e=None):
        title_text.value = "⚽ 축구 구단 목록"
        content_area.controls.clear()
        clubs = club_service.get_all_clubs()

        rows = ft.Row(wrap=True, spacing=12, run_spacing=12)
        for club in clubs:
            rows.controls.append(make_club_card(club))

        content_area.controls.append(rows)
        page.update()

    # =====================
    # 구단 검색
    # =====================
    def search_club(e=None):
        title_text.value = "🔍 구단 검색 결과"
        content_area.controls.clear()
        clubs = club_service.search_club(club_search_field.value)

        if not clubs:
            content_area.controls.append(ft.Text("검색 결과가 없습니다."))
        else:
            rows = ft.Row(wrap=True, spacing=12, run_spacing=12)
            for club in clubs:
                rows.controls.append(make_club_card(club))
            content_area.controls.append(rows)
        page.update()

    # =====================
    # 경기 조회
    # =====================
    def show_matches(e=None):
        title_text.value = "📅 경기 일정"
        content_area.controls.clear()
        matches = match_service.get_matches()
        match_dropdown.options.clear()

        for match in matches:
            match_dropdown.options.append(
                ft.dropdown.Option(
                    key=str(match["match_id"]),
                    text=f"{match['home_team']} VS {match['away_team']}"
                )
            )
            content_area.controls.append(
                ft.Card(
                    content=ft.Container(
                        padding=16,
                        content=ft.Column(
                            spacing=6,
                            controls=[
                                ft.Text(
                                    f"{match['home_team']}  VS  {match['away_team']}",
                                    size=16, weight="bold"
                                ),
                                ft.Text(str(match["match_time"]), size=12),
                                ft.Text(match["broadcast_platform"], size=12),
                            ]
                        )
                    )
                )
            )
        page.update()

    # =====================
    # 펍 조회
    # =====================
    def show_pubs(e=None):
        title_text.value = "🍺 펍 목록"
        content_area.controls.clear()
        pubs = pub_service.get_all_pubs()

        for pub in pubs:
            content_area.controls.append(
                ft.Card(
                    content=ft.Container(
                        padding=14,
                        content=ft.Column(
                            spacing=4,
                            controls=[
                                ft.Text(f"ID {pub['pub_id']}  {pub['pub_name']}",
                                        size=16, weight="bold"),
                                ft.Text(pub["address"], size=13),
                                ft.Text(pub["main_league"], size=12),
                                ft.Image(src=pub["pub_image_path"],
                                         width=200, height=120),
                            ]
                        )
                    )
                )
            )
        page.update()

    # =====================
    # 펍 추천
    # =====================
    def recommend_pub(e=None):
        title_text.value = "🎯 펍 추천"
        content_area.controls.clear()
        content_area.controls.append(
            ft.Row(
                spacing=10,
                controls=[
                    match_dropdown,
                    ft.ElevatedButton("추천 받기", on_click=_do_recommend)
                ]
            )
        )
        page.update()

    def _do_recommend(e):
        while len(content_area.controls) > 1:
            content_area.controls.pop()

        if match_dropdown.value is None:
            page.snack_bar = ft.SnackBar(ft.Text("경기를 먼저 선택하세요."))
            page.snack_bar.open = True
            page.update()
            return

        match_id = int(match_dropdown.value)
        pubs = pub_service.recommend_pubs(match_id)

        if pubs:
            content_area.controls.append(
                ft.Text(
                    f"{pubs[0]['home_team']} VS {pubs[0]['away_team']} 추천 펍",
                    size=18, weight="bold"
                )
            )

        for pub in pubs:
            content_area.controls.append(
                ft.Card(
                    content=ft.Container(
                        padding=14,
                        content=ft.Column(
                            spacing=4,
                            controls=[
                                ft.Text(pub["pub_name"], size=16, weight="bold"),
                                ft.Text(pub["address"], size=13),
                                ft.Text(pub["main_league"], size=12),
                                ft.Image(src=pub["pub_image_path"],
                                         width=200, height=120),
                            ]
                        )
                    )
                )
            )
        page.update()

    # =====================
    # 펍 관리 다이얼로그
    # =====================
    def close_pub_dialog(e):
        page.pop_dialog()

    pub_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("🍺 펍 관리", size=20, weight="bold"),
        content=ft.Container(
            width=420,
            content=ft.Column(
                tight=True, spacing=10,
                controls=[
                    pub_id_field, pub_name_field,
                    address_field, league_field, support_field, image_field,
                    ft.Row(
                        spacing=8,
                        controls=[
                            ft.ElevatedButton("펍 등록",
                                              on_click=lambda e: _pub_action("add")),
                            ft.ElevatedButton("펍 수정",
                                              on_click=lambda e: _pub_action("update")),
                            ft.ElevatedButton("펍 삭제",
                                              on_click=lambda e: _pub_action("delete")),
                        ]
                    )
                ]
            )
        ),
        actions=[ft.TextButton("닫기", on_click=close_pub_dialog)],
    )

    def _pub_action(action):
        if action == "add":
            pub_service.add_pub(pub_name_field.value, address_field.value,
                                league_field.value, int(support_field.value),
                                image_field.value)
            msg = "펍 등록 완료"
        elif action == "update":
            pub_service.update_pub(int(pub_id_field.value),
                                   address_field.value, league_field.value)
            msg = "펍 수정 완료"
        else:
            pub_service.delete_pub(int(pub_id_field.value))
            msg = "펍 삭제 완료"

        for f in [pub_id_field, pub_name_field, address_field, league_field, support_field, image_field]:
            f.value = ""

        page.snack_bar = ft.SnackBar(ft.Text(msg))
        page.snack_bar.open = True
        page.update()
        show_pubs()

    def open_pub_dialog(e):
        page.show_dialog(pub_dialog)

    # =====================
    # 구단 검색 다이얼로그
    # =====================
    def close_search_dialog(e):
        page.pop_dialog()

    def _do_search(e):
        close_search_dialog(e)
        search_club()

    search_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("🔍 구단 검색", size=20, weight="bold"),
        content=ft.Container(
            width=360,
            content=ft.Row(
                spacing=8,
                controls=[
                    club_search_field,
                    ft.ElevatedButton("검색", on_click=_do_search)
                ]
            )
        ),
        actions=[ft.TextButton("닫기", on_click=close_search_dialog)],
    )

    def open_search_dialog(e):
        page.show_dialog(search_dialog)

    # =====================
    # 시작 화면 (랜딩)
    # =====================
    def show_home(e=None):
        title_text.value = ""
        content_area.controls.clear()
        content_area.controls.append(
            ft.Container(
                padding=40,
                content=ft.Column(
                    horizontal_alignment="center",
                    spacing=18,
                    controls=[
                        ft.Text("⚽", size=70, text_align="center"),
                        ft.Text(
                            "해외축구(EPL) 시청 가이드에 오신 것을 환영합니다",
                            size=24, weight="bold", text_align="center"
                        ),
                        ft.Text(
                            "2025-26 시즌 EPL 경기 일정과 중계 정보를 확인하고,\n"
                            "내가 응원하는 팀의 경기를 함께 볼 수 있는 축구 펍을 추천받으세요.",
                            size=15, text_align="center", color="#AAAAAA"
                        ),
                        ft.Container(height=10),
                        ft.Text(
                            "👆 위의 버튼을 눌러 원하는 기능을 선택하세요",
                            size=14, weight="bold", text_align="center", color="#5B9BD5"
                        ),
                    ]
                )
            )
        )
        page.update()

    # =====================
    # 상단 네비게이션 (텍스트 버튼)
    # =====================
    nav_bar = ft.Row(
        wrap=True,
        spacing=6,
        run_spacing=6,
        controls=[
            ft.TextButton("🏠 홈", on_click=show_home),
            ft.TextButton("구단 목록", on_click=show_clubs),
            ft.TextButton("구단 검색", on_click=open_search_dialog),
            ft.TextButton("경기 일정", on_click=show_matches),
            ft.TextButton("펍 목록", on_click=show_pubs),
            ft.TextButton("펍 추천", on_click=recommend_pub),
            ft.TextButton("펍 관리", on_click=open_pub_dialog),
        ]
    )

    # =====================
    # 메인 레이아웃
    # =====================
    page.add(
        ft.Container(
            padding=16,
            content=ft.Column(
                spacing=12,
                controls=[
                    ft.Text("⚽ 해외축구(EPL) 시청 가이드", size=28, weight="bold"),
                    nav_bar,
                    ft.Divider(),
                    title_text,
                    content_area,
                ]
            ),
            expand=True,
        )
    )

    show_home()


ft.app(target=main)
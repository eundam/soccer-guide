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

    result_area = ft.Column()

    # =====================
    # 입력 필드
    # =====================

    pub_id_field = ft.TextField(
        label="펍 ID (수정/삭제용)"
    )
    match_dropdown = ft.Dropdown(
    label="추천받을 경기",
    width=300
)
    

    pub_name_field = ft.TextField(
        label="펍 이름"
    )

    address_field = ft.TextField(
        label="주소"
    )

    league_field = ft.TextField(
        label="주요 리그"
    )

    image_field = ft.TextField(
        label="이미지 경로"
    )
    club_search_field = ft.TextField(
        label="구단 검색"
    )
    date_field = ft.TextField(
        label="경기 날짜 (YYYY-MM-DD)"
)

    # =====================
    # 구단 조회
    # =====================

    def show_clubs(e):

        result_area.controls.clear()

        clubs = club_service.get_all_clubs()

        for club in clubs:

            result_area.controls.append(
                ft.Card(
                    content=ft.Container(
                        padding=10,
                        content=ft.Row([
                            ft.Image(
                                src=club["logo_path"],
                                width=60,
                                height=60
                            ),

                            ft.Column([
                                ft.Text(
                                    club["team_name"],
                                    size=18,
                                    weight="bold"
                                ),

                                ft.Text(
                                    club["league"]
                                ),

                                ft.Text(
                                    club["manager"]
                                )
                            ])
                        ])
                    )
                )
            )

        page.update()

    # =====================
    # 경기 조회
    # =====================

    def show_matches(e):

        result_area.controls.clear()

        matches = match_service.get_matches()

        match_dropdown.options.clear()

        for match in matches:

            match_dropdown.options.append(
                ft.dropdown.Option(
                    key=str(match["match_id"]),
                    text=f"{match['home_team']} VS {match['away_team']}"
        )
    )
        page.update()
        

        for match in matches:

            result_area.controls.append(
                ft.Card(
                    content=ft.Container(
                        padding=10,
                        content=ft.Column([
                            ft.Text(
                                f"{match['home_team']} VS {match['away_team']}",
                                size=18,
                                weight="bold"
                            ),

                            ft.Text(
                                str(match["match_time"])
                            ),

                            ft.Text(
                                match["broadcast_platform"]
                            )
                        ])
                    )
                )
            )

        page.update()

    # =====================
    # 펍 전체 조회
    # =====================

    def show_pubs(e):

        result_area.controls.clear()

        pubs = pub_service.get_all_pubs()

        for pub in pubs:

            result_area.controls.append(
                ft.Card(
                    content=ft.Container(
                        padding=10,
                        content=ft.Column([

                            ft.Text(
                                f"ID : {pub['pub_id']}",
                                weight="bold"
                            ),

                            ft.Text(
                                pub["pub_name"]
                            ),

                            ft.Text(
                                pub["address"]
                            ),

                            ft.Text(
                                pub["main_league"]
                            ),

                            ft.Image(
                                src=pub["pub_image_path"],
                                width=250
                            )
                        ])
                    )
                )
            )

        page.update()

    # =====================
    # 펍 등록
    # =====================

    def add_pub(e):

        pub_service.add_pub(
            pub_name_field.value,
            address_field.value,
            league_field.value,
            image_field.value
        )

        page.snack_bar = ft.SnackBar(
            ft.Text("펍 등록 완료")
        )

        page.snack_bar.open = True

        pub_name_field.value = ""
        address_field.value = ""
        league_field.value = ""
        image_field.value = ""

        
        page.update()
        show_pubs(None)

    # =====================
    # 펍 수정
    # =====================

    def update_pub(e):

        pub_service.update_pub(
            int(pub_id_field.value),
            address_field.value,
            league_field.value
        )

        page.snack_bar = ft.SnackBar(
            ft.Text("펍 수정 완료")
        )

        page.snack_bar.open = True
        page.update()
        show_pubs(None)

    # =====================
    # 펍 삭제
    # =====================

    def delete_pub(e):

        pub_service.delete_pub(
            int(pub_id_field.value)
        )

        page.snack_bar = ft.SnackBar(
            ft.Text("펍 삭제 완료")
        )

        page.snack_bar.open = True
        page.update()
        show_pubs(None)

    # =====================
    # JOIN 기반 펍 추천
    # =====================

    def recommend_pub(e):

        result_area.controls.clear()
        if match_dropdown.value is None:

            page.snack_bar = ft.SnackBar(
                ft.Text("경기를 먼저 선택하세요.")
            )

            page.snack_bar.open = True
            page.update()
            return

        match_id = int(match_dropdown.value)

        pubs = pub_service.recommend_pubs(match_id)
        

        if pubs:

            result_area.controls.append(
                ft.Text(
                    f"{pubs[0]['home_team']} VS {pubs[0]['away_team']}",
                    size=24,
                    weight="bold"
                )
            )

            # 추천 경기 정보 표시
            result_area.controls.append(
                ft.Text(
                    f"선택한 경기 ID : {match_id}",
                    size=20,
                    weight="bold"
                )
            )

        for pub in pubs:

            result_area.controls.append(
                ft.Card(
                    content=ft.Container(
                        padding=10,
                        content=ft.Column([

                            ft.Text(
                                pub["pub_name"],
                                size=18,
                                weight="bold"
                            ),

                            ft.Text(
                                pub["address"]
                            ),

                            ft.Text(
                                pub["main_league"]
                            ),

                            ft.Image(
                                src=pub["pub_image_path"],
                                width=250
                            )
                        ])
                    )
                )
            )

        page.update()

    def search_club(e):

        result_area.controls.clear()

        clubs = club_service.search_club(
            club_search_field.value
        )

        for club in clubs:

            result_area.controls.append(
                ft.Text(
                    club["team_name"]
                )
            )

        page.update()

    def search_match(e):

        result_area.controls.clear()

        matches = match_service.search_match_by_date(
            date_field.value
        )

        for match in matches:

            result_area.controls.append(
                ft.Text(
                    f"{match['home_team_id']} VS {match['away_team_id']}"
                )
            )

        page.update()

    # =====================
    # 화면 구성
    # =====================

    page.add(
        

        ft.Text(
            "⚽ 해외축구(EPL) 시청 가이드",
            size=30,
            weight="bold"
        ),

        ft.Row([
            # ft.ElevatedButton(
            #     "날짜 검색",
            #     on_click=search_match
            # ),

            ft.ElevatedButton(
                "구단 조회",
                on_click=show_clubs
            ),
            ft.ElevatedButton(
                "구단 검색",
                on_click=search_club
            ),

            ft.ElevatedButton(
                "경기 조회",
                on_click=show_matches
            ),

            ft.ElevatedButton(
                "펍 조회",
                on_click=show_pubs
            ),

            ft.ElevatedButton(
                "펍 추천",
                on_click=recommend_pub
            )

        ]),

        ft.Divider(),

        ft.Text(
            "펍 관리",
            size=20,
            weight="bold"
        ),

        pub_id_field,
        pub_name_field,
        address_field,
        league_field,
        image_field,
        match_dropdown,
        club_search_field,
        #date_field,

        ft.Row([

            ft.ElevatedButton(
                "펍 등록",
                on_click=add_pub
            ),

            ft.ElevatedButton(
                "펍 수정",
                on_click=update_pub
            ),

            ft.ElevatedButton(
                "펍 삭제",
                on_click=delete_pub
            )

        ]),

        ft.Divider(),

        result_area
    )


ft.app(target=main)
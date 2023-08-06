from django.utils.translation import ugettext_lazy as _

MENUS = {
    "NAV_MENU_CORE": [
        {
            "name": _("Requests for exemption"),
            "url": "#",
            "icon": "business_center",
            "root": True,
            "validators": [
                ("menu_generator.validators.user_has_permission", "fritak.view_menu"),
            ],
            "submenu": [
                {
                    "name": _("My requests"),
                    "url": "fritak_index",
                    "icon": "person",
                    "validators": [
                        (
                            "menu_generator.validators.user_has_permission",
                            "fritak.apply_exemptionrequest",
                        ),
                    ],
                },
                {
                    "name": _("Approve requests 1"),
                    "url": "fritak_check1",
                    "icon": "done",
                    "validators": [
                        (
                            "menu_generator.validators.user_has_permission",
                            "fritak.check1_exemptionrequest",
                        )
                    ],
                },
                {
                    "name": _("Approve requests 2"),
                    "url": "fritak_check2",
                    "icon": "done_all",
                    "validators": [
                        (
                            "menu_generator.validators.user_has_permission",
                            "fritak.check2_exemptionrequest",
                        )
                    ],
                },
                {
                    "name": _("Archive"),
                    "url": "fritak_archive",
                    "icon": "archive",
                    "validators": [
                        (
                            "menu_generator.validators.user_has_permission",
                            "fritak.view_archive",
                        )
                    ],
                },
            ],
        }
    ]
}

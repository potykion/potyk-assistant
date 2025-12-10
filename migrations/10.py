import sqlite3


def migrate(cursor: sqlite3.Cursor):
    cursor.executescript(
        """
        create table movies
        (
            id            integer not null
                constraint movies_pk
                    primary key autoincrement,
            title         TEXT,
            image         text,
            kinopoisk_url TEXT,
            download_url  TEXT,
            watch_url     TEXT,
            why           TEXT
        );
        INSERT INTO movies (title, image, kinopoisk_url, download_url, watch_url, why)
        VALUES ('Красивая работа',
                'https://avatars.mds.yandex.net/get-kinopoisk-image/1946459/2b9b671e-4558-4d08-b114-4d6ac79f26dd/3840x',
                'https://www.kinopoisk.ru/film/119363/', 'https://rutracker.org/forum/viewtopic.php?t=3010430/', null,
                'сигма-муви по мнению <a href="https://t.me/rzhavuykholodez/95">ржавого холодца</a>');
        INSERT INTO movies (title, image, kinopoisk_url, download_url, watch_url, why)
        VALUES ('Аркейн',
                'https://kinopoisk-ru.clstorage.net/q15e5R217/47fb3eu-/tg8pfLbyLiOnhorT74vfgCYfate9ba2gOdk8yhVaa2SXK2UQlA8PjEof2MUfZDduxPxqnCy7gbfzK8iTMfcqb9LLDE3mx9qXUgOvMp5evzXjy8uyCFz8dLztfRsgX46WZCnmMgMtbH7IHR7RK2A2y3EJnp1p3hXnEu_s1BeDTllmTMsflEIfRNTGSTetKN1DVs3_RW29i_BYyhkpx4g71LX6pyGD7A_feuy8Uxli4JuBqd7PCFxmRsVu7qamh7wqBt1qz3ahP_XndqukbyqfMERsTuZ__ioRKKq6aeTpCbeH6PZwYK8t7Lj9btEbsWEJcblOPtkO97WHXB9m1Vbdarbu-OxksY4XViS7ZzxYTsEn3l5WLcxqYmnKair1i8l2FNm3A3F-_2zr_z4hKzMziuE4TlybXxbntQ5NNESXP4r2TIn_RgBNhZYF63dOOa_BBDw8JM4vuZD5SJsZ9_uq1ad65qCyj44Myv-s4LlicIlRWB6cyl4F1bVOTNXWtk7LxixoXJWRv5flRhrWH5n9oHXOrQe__Eui68v426bI2zW0uOVwwn0t3fpNHWJrMXJY8xp83eqMxeTVfY_VlzRsOWT_OQ0EMU83NtZbZH7bDkJUXEylT2_r8MgoCnmF-svUxFs2QxGfvs0KrIyAiHLCC7PaHEzJT8b1Fy-uhqTnjWp3HMl9hUFdhWX0K4c82b8whM5-BS_tqMPq6_lIBTiqNLWqd3Jzny0e6y3sYQmBcEuT-Fys2w42Z3dtrxUmNwwY1P3pnSbB7jVXpAk13HucIPcOnkR9fGnyiKnqqHWqyzW36NTTcl9NjRieLzD6w6L78wovbPkflKdU3vwlNvWOWzVPSE8EU44Ftfa4xz-IvsFFTg1mTLxL0Ri6KuhE6Ar21JsmMhOOHxxKr9xQCuNQ-OEbnw97nBdW9wy8xSYnvhglX1scxIAeF7UEWNcuev4wJi5O1E4ee9A7G-kKJ0hLZ6RLtNFzj82sOs-e4thzMIhBqfwOOrxUt7etnfTHFQ84VKz7LpeCL-d219mGHVsP0NVO30Tcvpnjesi7ucdamNfnq-UwUoyf7klMjPJLsdBLUsj-z8o_F0VnfpzkpSTuWldMeh5koI-GxMW4lK8pHkJHPo103w3IYcs6-Cnl-pu3VRs1gACvby17_CxyC4JSeUAZnw5ZD6S2t64_RfV3rHkHvjvshmHtBtdnWTZtOU2DdF2eJT3-ilD4qVmKJQvaxoSKlLKDjc09aA9OospjMlqx6G_9yU5FpgT-_oVUxH_Zxzw7TTbx3GX2Fom13XuvkTQPvxUvzftiWOlbCaeKSzUn-PZRElyNP9hdXoLJc1M4g-m_floOl3amjG-U9rYf-3deiR-k8S31FzQ71gybDnBUD96VD72aQlgZ2lvESDiEhYsVUuLuPn76zK8hCkJQqVOrb_zrf4Sn1i6eJoa1Xgik3ime97G8tCUXWvdfCG0zJF2-t91uKPBb6euKJUirFObYVJLCPa0vy11sYStxYbpDaC686l-EVbd8XyTU1Z5bBS9bTleSr6c299r2DPv_MncdjXU_3MvB60kLi9abqgfVKubyAh_uDWivPtCIwfJ74bptzpm_F5d1np30lIVeCwSvyP8V41w1h9QLJe4rjUMnfg72HD3Ic2uYqyqFeenUt_plAHFNTM3Kn-7wKtHgO2KoHX34DkRmJU9NVZVn3YjnDxmNZmOOJgRFW4Rve0wC9t2cF-3eWMA6COiYFRibRYUIhoISfBwcyByO41rxoGnTWVzuezznV9TsvAbXRb4oZ2zZv7RwfLekRmu2btm9IKcurKTdTnhy-zpoOId564UkSIYxYC1frxlNnVN4cRD6w7pczBhcFaf2v80WRdbt62UPOl3VQo3nN3e4lg-a_zNXTLwUTe7ZovmoiMpnCgoX1Et1MbKfvT9LfNzS2lOzSGEYXO37rJVX9G5OlXcV7uvmvCoNJBGvZ_clyLfMiXwyJH5c5P4MuaC7CtuY94q5xXU7N0KzT6x_yT7fIdlxM0lQ6H1N6d-XxidcjPUkl-wJJWwbXlQDXWZV1Ju2rllMMFXuracfTPlC-gtKKhbKy6SGiPUjcV_dv1vNDiErExJp4AlsLyi8pHcnj6_HdVccGHZ-O91Esp62J8YJNSyKTgNnHAyVzYwKcGl665slWOjnxalkUuCPD90pzt9T2JOC-VE6f_zKfKeVJ5z_Z5VUbYoEvjo85HKvd4U1ifXMmzxyBA2OF54dunN4uvjKRThJB7UK97JSHa-tCk3-0LgjwuhR-Z6OKT72pKSuHubkZl34pQ7rnyQhvrVl9cn1LKjOAXXMXEedX0vx6fg4-IfrGRSHezaQEA8-b0k9DLFoIMEKYYhufLg-NdW2fY1Et2etWWZcy59mwpyGZ_b4pS9KbZNGfkxnjy16A-j4Ksp0-kuFVyr1EGL-rX0IT21i-3ExCsGJXs6aTqYmxL4M9mb3jzs2TshspfCuBAXF-0RNGq2gho98db4-m6C7C9oIZ_uLZoeJlrED323uK1zugsmB8JvRC699Sk-HxKYtvyT0Vc5oJb_ZPnTTjDckVktV7Pruw3Z-DaQcPrkQWsq6m5X7uaX1uFcTI72NH3turSBIUaMKoqusjhpvp0alP7_X1CTuCJe-u30mEAxVdYXp9kzoXENUP8z0He9JM2oqKQglmOi19cmnEvFdPs5qvV1jaSNRGOCrT0zYDmQlFj-uBrf1jso1fXtNFlJMd6b3ivUuma1yF-_fFk_tyFHoG_qbNYj7dLXpdoFinDxs6f29ABtiA2jw6jzcqQw2xARObXdkRk36hj8YzHQB79V2FErmTVr9kCcO3qZebcuS2tl6yZdKKtUkioZzo10-TRlt3ZCpETG54vscnspMJqX3Dn-1ZffOGSeNWA6E0D03BWb51Jw53mKl391HvAyaUCur-KoXWsjFpokHI0INv98YTo8COPMTi-A4L83775RFFWxPs',
                'https://www.kinopoisk.ru/series/4445150/', '', 'https://v4.fanfilm4k.media/3303-arkejn-2021.html',
                'Миха хвалит, все хвалят');
        """
    )
    cursor.connection.commit()

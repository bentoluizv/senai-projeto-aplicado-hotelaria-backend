INSERT INTO guest (document, created_at, name, surname, country, phone)
       VALUES
            ("00157624242", "2024-03-15T10:30:00", "Bento Luiz", "Machado da Silva Neto", "Brazil", "48992054211"),
            ("17323163927", "2024-03-16T10:30:00", "Fernando", "Oda", "Brazil", "48999766022"),
            ("71807137910", "2024-03-16T10:50:00", "Guilherme", "Oda", "Brazil", "48991696813"),
            ("65922869973", "2024-01-12T10:00:00", "Valério", "Piana", "Brazil", "48932395808");

INSERT INTO accommodation (uuid, created_at, status, name, total_guests, single_beds, double_beds, min_nights, price)
       VALUES
            ("bcadaaf8-a036-42d5-870c-de7b24792abf", "2000-01-01T00:00:00", "Disponível", "Domo", 3, 0, 1, 2, 590),
            ("d09ff9fa-92cc-42b4-9422-0df35a40b5ad", "2000-01-01T00:03:00", "Disponível", "Charrua (Bus)", 2, 0, 1, 2, 490),
            ("618b58c5-c6f7-4bfe-bd33-a143757f149d", "2000-01-01T00:06:00", "Disponível", "Suíte Com Cozinha", 3, 1, 1, 2, 390),
            ("b18ffd67-a84f-4da9-86e0-20ad8e814ef9", "2000-01-01T00:08:00", "Disponível", "Chalé família", 5, 1, 2, 2, 590),
            ("db626d38-4372-43c0-bba1-29ea06c540c2", "2000-01-01T00:12:00", "Disponível", "Cabana", 3, 1, 1, 2, 490),
            ("242d5665-aa90-429a-95d5-767515ff8ccc", "2000-01-01T00:15:00", "Disponível", "Estacionamento para overlanders", 4, 0, 0, 2, 100);

INSERT INTO amenities (amenitie)
       VALUES
            ("ar-condicionado"),
            ("wifi"),
            ("tv"),
            ("frigobar"),
            ("ducha"),
            ("cozinha"),
            ("toalhas"),
            ("banheira");

INSERT INTO amenities_per_accommodation (accommodation_uuid, amenitie_name)
       VALUES
            ("bcadaaf8-a036-42d5-870c-de7b24792abf", "ar-condicionado"),
            ("bcadaaf8-a036-42d5-870c-de7b24792abf", "wifi"),
            ("bcadaaf8-a036-42d5-870c-de7b24792abf", "tv"),
            ("bcadaaf8-a036-42d5-870c-de7b24792abf", "frigobar"),
            ("bcadaaf8-a036-42d5-870c-de7b24792abf", "ducha"),
            ("bcadaaf8-a036-42d5-870c-de7b24792abf", "cozinha"),
            ("bcadaaf8-a036-42d5-870c-de7b24792abf", "toalhas"),
            ("d09ff9fa-92cc-42b4-9422-0df35a40b5ad", "ar-condicionado"),
            ("d09ff9fa-92cc-42b4-9422-0df35a40b5ad", "wifi"),
            ("d09ff9fa-92cc-42b4-9422-0df35a40b5ad", "tv"),
            ("d09ff9fa-92cc-42b4-9422-0df35a40b5ad", "frigobar"),
            ("d09ff9fa-92cc-42b4-9422-0df35a40b5ad", "ducha"),
            ("d09ff9fa-92cc-42b4-9422-0df35a40b5ad", "cozinha"),
            ("d09ff9fa-92cc-42b4-9422-0df35a40b5ad", "toalhas"),
            ("d09ff9fa-92cc-42b4-9422-0df35a40b5ad", "banheira"),
            ("618b58c5-c6f7-4bfe-bd33-a143757f149d", "ar-condicionado"),
            ("618b58c5-c6f7-4bfe-bd33-a143757f149d", "wifi"),
            ("618b58c5-c6f7-4bfe-bd33-a143757f149d", "tv"),
            ("618b58c5-c6f7-4bfe-bd33-a143757f149d", "cozinha"),
            ("618b58c5-c6f7-4bfe-bd33-a143757f149d", "toalhas"),
            ("b18ffd67-a84f-4da9-86e0-20ad8e814ef9", "ar-condicionado"),
            ("b18ffd67-a84f-4da9-86e0-20ad8e814ef9", "wifi"),
            ("b18ffd67-a84f-4da9-86e0-20ad8e814ef9", "tv"),
            ("b18ffd67-a84f-4da9-86e0-20ad8e814ef9", "cozinha"),
            ("b18ffd67-a84f-4da9-86e0-20ad8e814ef9", "toalhas"),
            ("db626d38-4372-43c0-bba1-29ea06c540c2", "ar-condicionado"),
            ("db626d38-4372-43c0-bba1-29ea06c540c2", "wifi"),
            ("db626d38-4372-43c0-bba1-29ea06c540c2", "tv"),
            ("db626d38-4372-43c0-bba1-29ea06c540c2", "cozinha"),
            ("db626d38-4372-43c0-bba1-29ea06c540c2", "toalhas"),
            ("242d5665-aa90-429a-95d5-767515ff8ccc", "ducha");

INSERT INTO booking (uuid, created_at, status, check_in, check_out, document, accommodation_uuid)
        VALUES
            ("e08f76e8-0e71-4a48-a85a-bf7e8f61479e", "2024-06-02T12:30:12", "Aguardando Check-In",  "2024-06-15T08:30:00", "2024-06-18T17:30:00", "00157624242", "242d5665-aa90-429a-95d5-767515ff8ccc"),
            ("92f2f5bb-6cac-4485-a43e-6927213f662f", "2024-06-05T12:30:12", "Aguardando Check-In", "2024-06-15T08:30:00", "2024-06-18T17:30:00", "17323163927", "618b58c5-c6f7-4bfe-bd33-a143757f149d"),
            ("1da32904-b059-4d00-a5c3-6538f75619e7", "2024-06-05T12:35:12", "Aguardando Check-In", "2024-06-15T08:30:00", "2024-06-18T17:30:00", "71807137910", "bcadaaf8-a036-42d5-870c-de7b24792abf"),
            ("fd49432c-a03a-40d3-9082-9efeb8a6332c", "2024-06-01T08:35:42", "Ativa", "2024-06-15T08:30:00", "2024-06-28T17:30:00", "65922869973", "b18ffd67-a84f-4da9-86e0-20ad8e814ef9");
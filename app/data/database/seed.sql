INSERT INTO guest (document, created_at, name, surname, country, phone)
       VALUES
            ("00157624242", "2024-03-15T10:30:00", "Bento", "Rocha", "Brazil", "48xxxxxxxxx"),
            ("17323163927", "2024-03-16T10:30:00", "Fernando", "Salim", "Brazil", "48xxxxxxxxx"),
            ("71807137910", "2024-03-16T10:50:00", "Julio", "Silva", "Brazil", "48xxxxxxxxx"),
            ("65922869973", "2024-01-12T10:00:00", "Valério", "Pena", "Brazil", "48xxxxxxxxx");

INSERT INTO accommodation (created_at, status, name, total_guests, single_beds, double_beds, min_nights, price)
       VALUES
            ("2000-01-01T00:00:00", "Disponível", "Domo", 3, 0, 1, 2, 590),
            ("2000-01-01T00:03:00", "Disponível", "Charrua (Bus)", 2, 0, 1, 2, 490),
            ("2000-01-01T00:06:00", "Disponível", "Suíte Com Cozinha", 3, 1, 1, 2, 390),
            ("2000-01-01T00:08:00", "Disponível", "Chalé família", 5, 1, 2, 2, 590),
            ("2000-01-01T00:12:00", "Disponível", "Cabana", 3, 1, 1, 2, 490),
            ("2000-01-01T00:15:00", "Disponível", "Estacionamento para overlanders", 4, 0, 0, 2, 100);

INSERT INTO amenities (name)
       VALUES
            ("ar-condicionado"),
            ("wifi"),
            ("tv"),
            ("frigobar"),
            ("ducha"),
            ("cozinha"),
            ("toalhas"),
            ("banheira");

INSERT INTO amenities_per_accommodation (accommodation_id, amenitie_id)
       VALUES
            (1, 1),
            (1, 2),
            (1, 3),
            (1, 4),
            (1, 5),
            (1, 6),
            (1, 7),
            (2, 1),
            (2, 2),
            (2, 3),
            (2, 4),
            (2, 5),
            (2, 6),
            (2, 7),
            (2, 8),
            (3, 1),
            (3, 2),
            (3, 3),
            (3, 6),
            (3, 7),
            (4, 1),
            (4, 2),
            (4, 3),
            (4, 6),
            (4, 7),
            (5, 1),
            (5, 2),
            (5, 3),
            (5, 6),
            (5, 7),
            (6, 5);

INSERT INTO booking (uuid, created_at, locator, status, check_in, check_out, guest_document, accommodation_id, budget)
        VALUES
            ("e08f76e8-0e71-4a48-a85a-bf7e8f61479e", "2024-06-02T12:30:12", "AB897564", "Aguardando Check-In",  "2024-06-15T08:30:00", "2024-06-18T17:30:00", "00157624242", 6, 0),
            ("92f2f5bb-6cac-4485-a43e-6927213f662f", "2024-06-05T12:30:12", "AA978531", "Aguardando Check-In", "2024-06-15T08:30:00", "2024-06-18T17:30:00", "17323163927", 3, 0),
            ("1da32904-b059-4d00-a5c3-6538f75619e7", "2024-06-05T12:35:12", "DS273845", "Aguardando Check-In", "2024-06-15T08:30:00", "2024-06-18T17:30:00", "71807137910", 1, 0),
            ("fd49432c-a03a-40d3-9082-9efeb8a6332c", "2024-06-01T08:35:42", "GF965283", "Ativa", "2024-06-15T08:30:00", "2024-06-28T17:30:00", "65922869973", 4, 0);
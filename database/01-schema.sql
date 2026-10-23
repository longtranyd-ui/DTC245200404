-- Chi tao cau truc, khong chen du lieu mau.
CREATE TABLE customers (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    full_name varchar(120) NOT NULL CHECK (length(trim(full_name)) > 0),
    phone varchar(30) NOT NULL CHECK (length(trim(phone)) > 0)
);
CREATE TABLE pets (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name varchar(100) NOT NULL CHECK (length(trim(name)) > 0),
    species varchar(80) NOT NULL CHECK (length(trim(species)) > 0),
    customer_id bigint NOT NULL REFERENCES customers(id) ON DELETE RESTRICT
);
CREATE TABLE services (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name varchar(120) NOT NULL CHECK (length(trim(name)) > 0),
    price numeric(12,2) NOT NULL CHECK (price >= 0),
    duration_minutes integer NOT NULL CHECK (duration_minutes > 0)
);
CREATE TABLE appointments (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    pet_id bigint NOT NULL REFERENCES pets(id) ON DELETE RESTRICT,
    service_id bigint NOT NULL REFERENCES services(id) ON DELETE RESTRICT,
    starts_at timestamptz NOT NULL,
    status varchar(20) NOT NULL CHECK (status IN ('scheduled', 'completed', 'cancelled'))
);

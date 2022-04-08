--
-- PostgreSQL database dump
--

-- Dumped from database version 13.2
-- Dumped by pg_dump version 13.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO postgres;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: hub_customer; Type: TABLE; Schema: public; Owner: kevlinsky
--

CREATE TABLE public.hub_customer (
    id integer NOT NULL,
    bk integer NOT NULL,
    created_at date NOT NULL,
    closed_at date
);


ALTER TABLE public.hub_customer OWNER TO kevlinsky;

--
-- Name: hub_product; Type: TABLE; Schema: public; Owner: kevlinsky
--

CREATE TABLE public.hub_product (
    id integer NOT NULL,
    bk integer NOT NULL,
    created_at date NOT NULL,
    closed_at date
);


ALTER TABLE public.hub_product OWNER TO kevlinsky;

--
-- Name: hub_product_bk_seq; Type: SEQUENCE; Schema: public; Owner: kevlinsky
--

CREATE SEQUENCE public.hub_product_bk_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.hub_product_bk_seq OWNER TO kevlinsky;

--
-- Name: hub_product_bk_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kevlinsky
--

ALTER SEQUENCE public.hub_product_bk_seq OWNED BY public.hub_product.bk;


--
-- Name: hub_product_id_seq; Type: SEQUENCE; Schema: public; Owner: kevlinsky
--

CREATE SEQUENCE public.hub_product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.hub_product_id_seq OWNER TO kevlinsky;

--
-- Name: hub_product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kevlinsky
--

ALTER SEQUENCE public.hub_product_id_seq OWNED BY public.hub_product.id;


--
-- Name: hub_receipt; Type: TABLE; Schema: public; Owner: kevlinsky
--

CREATE TABLE public.hub_receipt (
    id integer NOT NULL,
    bk integer NOT NULL,
    created_at date NOT NULL,
    closed_at date
);


ALTER TABLE public.hub_receipt OWNER TO kevlinsky;

--
-- Name: hub_receipt_bk_seq; Type: SEQUENCE; Schema: public; Owner: kevlinsky
--

CREATE SEQUENCE public.hub_receipt_bk_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.hub_receipt_bk_seq OWNER TO kevlinsky;

--
-- Name: hub_receipt_bk_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kevlinsky
--

ALTER SEQUENCE public.hub_receipt_bk_seq OWNED BY public.hub_receipt.bk;


--
-- Name: hub_receipt_id_seq; Type: SEQUENCE; Schema: public; Owner: kevlinsky
--

CREATE SEQUENCE public.hub_receipt_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.hub_receipt_id_seq OWNER TO kevlinsky;

--
-- Name: hub_receipt_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kevlinsky
--

ALTER SEQUENCE public.hub_receipt_id_seq OWNED BY public.hub_receipt.id;


--
-- Name: hub_shop; Type: TABLE; Schema: public; Owner: kevlinsky
--

CREATE TABLE public.hub_shop (
    id integer NOT NULL,
    bk integer NOT NULL,
    created_at date NOT NULL,
    closed_at date
);


ALTER TABLE public.hub_shop OWNER TO kevlinsky;

--
-- Name: hub_shop_bk_seq; Type: SEQUENCE; Schema: public; Owner: kevlinsky
--

CREATE SEQUENCE public.hub_shop_bk_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.hub_shop_bk_seq OWNER TO kevlinsky;

--
-- Name: hub_shop_bk_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kevlinsky
--

ALTER SEQUENCE public.hub_shop_bk_seq OWNED BY public.hub_shop.bk;


--
-- Name: hub_shop_id_seq; Type: SEQUENCE; Schema: public; Owner: kevlinsky
--

CREATE SEQUENCE public.hub_shop_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.hub_shop_id_seq OWNER TO kevlinsky;

--
-- Name: hub_shop_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kevlinsky
--

ALTER SEQUENCE public.hub_shop_id_seq OWNED BY public.hub_shop.id;


--
-- Name: link_customer_receipt; Type: TABLE; Schema: public; Owner: kevlinsky
--

CREATE TABLE public.link_customer_receipt (
    customer_id integer NOT NULL,
    receipt_id integer,
    created_at date NOT NULL,
    closed_at date
);


ALTER TABLE public.link_customer_receipt OWNER TO kevlinsky;

--
-- Name: link_product_receipt; Type: TABLE; Schema: public; Owner: kevlinsky
--

CREATE TABLE public.link_product_receipt (
    product_id integer NOT NULL,
    receipt_id integer NOT NULL,
    created_at date NOT NULL,
    closed_at date
);


ALTER TABLE public.link_product_receipt OWNER TO kevlinsky;

--
-- Name: link_shop_receipt; Type: TABLE; Schema: public; Owner: kevlinsky
--

CREATE TABLE public.link_shop_receipt (
    shop_id integer NOT NULL,
    receipt_id integer NOT NULL,
    created_at date NOT NULL,
    closed_at date
);


ALTER TABLE public.link_shop_receipt OWNER TO kevlinsky;

--
-- Name: satellite_customer; Type: TABLE; Schema: public; Owner: kevlinsky
--

CREATE TABLE public.satellite_customer (
    customer_id integer NOT NULL,
    first_name character varying NOT NULL,
    last_name character varying NOT NULL,
    gender boolean NOT NULL,
    birth_date date NOT NULL,
    from_date date NOT NULL,
    to_date date
);


ALTER TABLE public.satellite_customer OWNER TO kevlinsky;

--
-- Name: satellite_customer_bk_seq; Type: SEQUENCE; Schema: public; Owner: kevlinsky
--

CREATE SEQUENCE public.satellite_customer_bk_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.satellite_customer_bk_seq OWNER TO kevlinsky;

--
-- Name: satellite_customer_bk_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kevlinsky
--

ALTER SEQUENCE public.satellite_customer_bk_seq OWNED BY public.hub_customer.bk;


--
-- Name: satellite_customer_id_seq; Type: SEQUENCE; Schema: public; Owner: kevlinsky
--

CREATE SEQUENCE public.satellite_customer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.satellite_customer_id_seq OWNER TO kevlinsky;

--
-- Name: satellite_customer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kevlinsky
--

ALTER SEQUENCE public.satellite_customer_id_seq OWNED BY public.hub_customer.id;


--
-- Name: satellite_product; Type: TABLE; Schema: public; Owner: kevlinsky
--

CREATE TABLE public.satellite_product (
    product_id integer NOT NULL,
    title character varying NOT NULL,
    description character varying NOT NULL,
    price double precision NOT NULL,
    discount double precision NOT NULL,
    supplier character varying NOT NULL,
    from_date date NOT NULL,
    to_date date
);


ALTER TABLE public.satellite_product OWNER TO kevlinsky;

--
-- Name: satellite_receipt; Type: TABLE; Schema: public; Owner: kevlinsky
--

CREATE TABLE public.satellite_receipt (
    receipt_id integer NOT NULL,
    amount integer NOT NULL,
    total_price double precision NOT NULL,
    from_date date NOT NULL,
    to_date date
);


ALTER TABLE public.satellite_receipt OWNER TO kevlinsky;

--
-- Name: satellite_shop; Type: TABLE; Schema: public; Owner: kevlinsky
--

CREATE TABLE public.satellite_shop (
    shop_id integer NOT NULL,
    description character varying NOT NULL,
    postal_code integer NOT NULL,
    employee_count integer NOT NULL,
    from_date date NOT NULL,
    to_date date
);


ALTER TABLE public.satellite_shop OWNER TO kevlinsky;

--
-- Name: hub_customer id; Type: DEFAULT; Schema: public; Owner: kevlinsky
--

ALTER TABLE ONLY public.hub_customer ALTER COLUMN id SET DEFAULT nextval('public.satellite_customer_id_seq'::regclass);


--
-- Name: hub_customer bk; Type: DEFAULT; Schema: public; Owner: kevlinsky
--

ALTER TABLE ONLY public.hub_customer ALTER COLUMN bk SET DEFAULT nextval('public.satellite_customer_bk_seq'::regclass);


--
-- Name: hub_product id; Type: DEFAULT; Schema: public; Owner: kevlinsky
--

ALTER TABLE ONLY public.hub_product ALTER COLUMN id SET DEFAULT nextval('public.hub_product_id_seq'::regclass);


--
-- Name: hub_product bk; Type: DEFAULT; Schema: public; Owner: kevlinsky
--

ALTER TABLE ONLY public.hub_product ALTER COLUMN bk SET DEFAULT nextval('public.hub_product_bk_seq'::regclass);


--
-- Name: hub_receipt id; Type: DEFAULT; Schema: public; Owner: kevlinsky
--

ALTER TABLE ONLY public.hub_receipt ALTER COLUMN id SET DEFAULT nextval('public.hub_receipt_id_seq'::regclass);


--
-- Name: hub_receipt bk; Type: DEFAULT; Schema: public; Owner: kevlinsky
--

ALTER TABLE ONLY public.hub_receipt ALTER COLUMN bk SET DEFAULT nextval('public.hub_receipt_bk_seq'::regclass);


--
-- Name: hub_shop id; Type: DEFAULT; Schema: public; Owner: kevlinsky
--

ALTER TABLE ONLY public.hub_shop ALTER COLUMN id SET DEFAULT nextval('public.hub_shop_id_seq'::regclass);


--
-- Name: hub_shop bk; Type: DEFAULT; Schema: public; Owner: kevlinsky
--

ALTER TABLE ONLY public.hub_shop ALTER COLUMN bk SET DEFAULT nextval('public.hub_shop_bk_seq'::regclass);


--
-- Data for Name: hub_customer; Type: TABLE DATA; Schema: public; Owner: kevlinsky
--

COPY public.hub_customer (id, bk, created_at, closed_at) FROM stdin;
\.


--
-- Data for Name: hub_product; Type: TABLE DATA; Schema: public; Owner: kevlinsky
--

COPY public.hub_product (id, bk, created_at, closed_at) FROM stdin;
\.


--
-- Data for Name: hub_receipt; Type: TABLE DATA; Schema: public; Owner: kevlinsky
--

COPY public.hub_receipt (id, bk, created_at, closed_at) FROM stdin;
\.


--
-- Data for Name: hub_shop; Type: TABLE DATA; Schema: public; Owner: kevlinsky
--

COPY public.hub_shop (id, bk, created_at, closed_at) FROM stdin;
\.


--
-- Data for Name: link_customer_receipt; Type: TABLE DATA; Schema: public; Owner: kevlinsky
--

COPY public.link_customer_receipt (customer_id, receipt_id, created_at, closed_at) FROM stdin;
\.


--
-- Data for Name: link_product_receipt; Type: TABLE DATA; Schema: public; Owner: kevlinsky
--

COPY public.link_product_receipt (product_id, receipt_id, created_at, closed_at) FROM stdin;
\.


--
-- Data for Name: link_shop_receipt; Type: TABLE DATA; Schema: public; Owner: kevlinsky
--

COPY public.link_shop_receipt (shop_id, receipt_id, created_at, closed_at) FROM stdin;
\.


--
-- Data for Name: satellite_customer; Type: TABLE DATA; Schema: public; Owner: kevlinsky
--

COPY public.satellite_customer (customer_id, first_name, last_name, gender, birth_date, from_date, to_date) FROM stdin;
\.


--
-- Data for Name: satellite_product; Type: TABLE DATA; Schema: public; Owner: kevlinsky
--

COPY public.satellite_product (product_id, title, description, price, discount, supplier, from_date, to_date) FROM stdin;
\.


--
-- Data for Name: satellite_receipt; Type: TABLE DATA; Schema: public; Owner: kevlinsky
--

COPY public.satellite_receipt (receipt_id, amount, total_price, from_date, to_date) FROM stdin;
\.


--
-- Data for Name: satellite_shop; Type: TABLE DATA; Schema: public; Owner: kevlinsky
--

COPY public.satellite_shop (shop_id, description, postal_code, employee_count, from_date, to_date) FROM stdin;
\.


--
-- Name: hub_product_bk_seq; Type: SEQUENCE SET; Schema: public; Owner: kevlinsky
--

SELECT pg_catalog.setval('public.hub_product_bk_seq', 1, false);


--
-- Name: hub_product_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kevlinsky
--

SELECT pg_catalog.setval('public.hub_product_id_seq', 1, false);


--
-- Name: hub_receipt_bk_seq; Type: SEQUENCE SET; Schema: public; Owner: kevlinsky
--

SELECT pg_catalog.setval('public.hub_receipt_bk_seq', 1, false);


--
-- Name: hub_receipt_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kevlinsky
--

SELECT pg_catalog.setval('public.hub_receipt_id_seq', 1, false);


--
-- Name: hub_shop_bk_seq; Type: SEQUENCE SET; Schema: public; Owner: kevlinsky
--

SELECT pg_catalog.setval('public.hub_shop_bk_seq', 1, false);


--
-- Name: hub_shop_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kevlinsky
--

SELECT pg_catalog.setval('public.hub_shop_id_seq', 1, false);


--
-- Name: satellite_customer_bk_seq; Type: SEQUENCE SET; Schema: public; Owner: kevlinsky
--

SELECT pg_catalog.setval('public.satellite_customer_bk_seq', 1, false);


--
-- Name: satellite_customer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kevlinsky
--

SELECT pg_catalog.setval('public.satellite_customer_id_seq', 1, false);


--
-- Name: hub_product hub_product_pk; Type: CONSTRAINT; Schema: public; Owner: kevlinsky
--

ALTER TABLE ONLY public.hub_product
    ADD CONSTRAINT hub_product_pk PRIMARY KEY (id);


--
-- Name: hub_receipt hub_receipt_pk; Type: CONSTRAINT; Schema: public; Owner: kevlinsky
--

ALTER TABLE ONLY public.hub_receipt
    ADD CONSTRAINT hub_receipt_pk PRIMARY KEY (id);


--
-- Name: hub_shop hub_shop_pk; Type: CONSTRAINT; Schema: public; Owner: kevlinsky
--

ALTER TABLE ONLY public.hub_shop
    ADD CONSTRAINT hub_shop_pk PRIMARY KEY (id);


--
-- Name: hub_customer satellite_customer_pk; Type: CONSTRAINT; Schema: public; Owner: kevlinsky
--

ALTER TABLE ONLY public.hub_customer
    ADD CONSTRAINT satellite_customer_pk PRIMARY KEY (id);


--
-- Name: hub_product_id_uindex; Type: INDEX; Schema: public; Owner: kevlinsky
--

CREATE UNIQUE INDEX hub_product_id_uindex ON public.hub_product USING btree (id);


--
-- Name: hub_receipt_id_uindex; Type: INDEX; Schema: public; Owner: kevlinsky
--

CREATE UNIQUE INDEX hub_receipt_id_uindex ON public.hub_receipt USING btree (id);


--
-- Name: hub_shop_id_uindex; Type: INDEX; Schema: public; Owner: kevlinsky
--

CREATE UNIQUE INDEX hub_shop_id_uindex ON public.hub_shop USING btree (id);


--
-- Name: satellite_customer_bk_uindex; Type: INDEX; Schema: public; Owner: kevlinsky
--

CREATE UNIQUE INDEX satellite_customer_bk_uindex ON public.hub_customer USING btree (bk);


--
-- Name: satellite_customer_id_uindex; Type: INDEX; Schema: public; Owner: kevlinsky
--

CREATE UNIQUE INDEX satellite_customer_id_uindex ON public.hub_customer USING btree (id);


--
-- Name: link_customer_receipt link_customer_receipt_hub_customer_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: kevlinsky
--

ALTER TABLE ONLY public.link_customer_receipt
    ADD CONSTRAINT link_customer_receipt_hub_customer_id_fk FOREIGN KEY (customer_id) REFERENCES public.hub_customer(id);


--
-- Name: link_customer_receipt link_customer_receipt_hub_receipt_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: kevlinsky
--

ALTER TABLE ONLY public.link_customer_receipt
    ADD CONSTRAINT link_customer_receipt_hub_receipt_id_fk FOREIGN KEY (receipt_id) REFERENCES public.hub_receipt(id);


--
-- Name: link_product_receipt link_product_receipt_hub_product_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: kevlinsky
--

ALTER TABLE ONLY public.link_product_receipt
    ADD CONSTRAINT link_product_receipt_hub_product_id_fk FOREIGN KEY (product_id) REFERENCES public.hub_product(id);


--
-- Name: link_product_receipt link_product_receipt_hub_receipt_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: kevlinsky
--

ALTER TABLE ONLY public.link_product_receipt
    ADD CONSTRAINT link_product_receipt_hub_receipt_id_fk FOREIGN KEY (receipt_id) REFERENCES public.hub_receipt(id);


--
-- Name: link_shop_receipt link_shop_receipt_hub_receipt_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: kevlinsky
--

ALTER TABLE ONLY public.link_shop_receipt
    ADD CONSTRAINT link_shop_receipt_hub_receipt_id_fk FOREIGN KEY (receipt_id) REFERENCES public.hub_receipt(id);


--
-- Name: link_shop_receipt link_shop_receipt_hub_shop_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: kevlinsky
--

ALTER TABLE ONLY public.link_shop_receipt
    ADD CONSTRAINT link_shop_receipt_hub_shop_id_fk FOREIGN KEY (shop_id) REFERENCES public.hub_shop(id);


--
-- Name: satellite_customer satellite_customer_hub_customer_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: kevlinsky
--

ALTER TABLE ONLY public.satellite_customer
    ADD CONSTRAINT satellite_customer_hub_customer_id_fk FOREIGN KEY (customer_id) REFERENCES public.hub_customer(id);


--
-- Name: satellite_product satellite_product_hub_product_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: kevlinsky
--

ALTER TABLE ONLY public.satellite_product
    ADD CONSTRAINT satellite_product_hub_product_id_fk FOREIGN KEY (product_id) REFERENCES public.hub_product(id);


--
-- Name: satellite_receipt satellite_receipt_hub_receipt_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: kevlinsky
--

ALTER TABLE ONLY public.satellite_receipt
    ADD CONSTRAINT satellite_receipt_hub_receipt_id_fk FOREIGN KEY (receipt_id) REFERENCES public.hub_receipt(id);


--
-- Name: satellite_shop satellite_shop_hub_shop_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: kevlinsky
--

ALTER TABLE ONLY public.satellite_shop
    ADD CONSTRAINT satellite_shop_hub_shop_id_fk FOREIGN KEY (shop_id) REFERENCES public.hub_shop(id);


--
-- PostgreSQL database dump complete
--


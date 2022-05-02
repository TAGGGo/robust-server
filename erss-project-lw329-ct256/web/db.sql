--
-- PostgreSQL database dump
--

-- Dumped from database version 14.1 (Debian 14.1-1.pgdg110+1)
-- Dumped by pg_dump version 14.2 (Debian 14.2-1.pgdg110+1)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: amazon_cart; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.amazon_cart (
    id bigint NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.amazon_cart OWNER TO postgres;

--
-- Name: amazon_cart_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.amazon_cart_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.amazon_cart_id_seq OWNER TO postgres;

--
-- Name: amazon_cart_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.amazon_cart_id_seq OWNED BY public.amazon_cart.id;


--
-- Name: amazon_cartproduct; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.amazon_cartproduct (
    id bigint NOT NULL,
    count integer NOT NULL,
    cart_id bigint NOT NULL,
    product_id bigint NOT NULL
);


ALTER TABLE public.amazon_cartproduct OWNER TO postgres;

--
-- Name: amazon_cartproduct_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.amazon_cartproduct_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.amazon_cartproduct_id_seq OWNER TO postgres;

--
-- Name: amazon_cartproduct_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.amazon_cartproduct_id_seq OWNED BY public.amazon_cartproduct.id;


--
-- Name: amazon_category; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.amazon_category (
    id bigint NOT NULL,
    cat_name character varying(50) NOT NULL,
    description character varying(50)
);


ALTER TABLE public.amazon_category OWNER TO postgres;

--
-- Name: amazon_category_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.amazon_category_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.amazon_category_id_seq OWNER TO postgres;

--
-- Name: amazon_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.amazon_category_id_seq OWNED BY public.amazon_category.id;


--
-- Name: amazon_customer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.amazon_customer (
    id bigint NOT NULL,
    phone character varying(20),
    address character varying(30),
    state character varying(30),
    country character varying(30),
    user_id integer NOT NULL,
    ups_name character varying(50)
);


ALTER TABLE public.amazon_customer OWNER TO postgres;

--
-- Name: amazon_customer_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.amazon_customer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.amazon_customer_id_seq OWNER TO postgres;

--
-- Name: amazon_customer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.amazon_customer_id_seq OWNED BY public.amazon_customer.id;


--
-- Name: amazon_order; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.amazon_order (
    id bigint NOT NULL,
    status character varying(15) NOT NULL,
    ups_name character varying(20),
    shipid_or_packageid bigint NOT NULL,
    truck_id integer,
    dest_x integer NOT NULL,
    dest_y integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    packed_at timestamp with time zone,
    loaded_at timestamp with time zone,
    delievered_at timestamp with time zone,
    user_id bigint NOT NULL,
    warehouse_id bigint
);


ALTER TABLE public.amazon_order OWNER TO postgres;

--
-- Name: amazon_order_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.amazon_order_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.amazon_order_id_seq OWNER TO postgres;

--
-- Name: amazon_order_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.amazon_order_id_seq OWNED BY public.amazon_order.id;


--
-- Name: amazon_orderproduct; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.amazon_orderproduct (
    id bigint NOT NULL,
    count integer NOT NULL,
    order_id bigint NOT NULL,
    product_id bigint NOT NULL
);


ALTER TABLE public.amazon_orderproduct OWNER TO postgres;

--
-- Name: amazon_orderproduct_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.amazon_orderproduct_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.amazon_orderproduct_id_seq OWNER TO postgres;

--
-- Name: amazon_orderproduct_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.amazon_orderproduct_id_seq OWNED BY public.amazon_orderproduct.id;


--
-- Name: amazon_product; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.amazon_product (
    id bigint NOT NULL,
    name character varying(50) NOT NULL,
    price integer NOT NULL,
    description character varying(50),
    photo character varying(100) NOT NULL,
    category_id bigint NOT NULL
);


ALTER TABLE public.amazon_product OWNER TO postgres;

--
-- Name: amazon_product_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.amazon_product_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.amazon_product_id_seq OWNER TO postgres;

--
-- Name: amazon_product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.amazon_product_id_seq OWNED BY public.amazon_product.id;


--
-- Name: amazon_warehouse; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.amazon_warehouse (
    id bigint NOT NULL,
    x integer NOT NULL,
    y integer NOT NULL
);


ALTER TABLE public.amazon_warehouse OWNER TO postgres;

--
-- Name: amazon_warehouse_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.amazon_warehouse_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.amazon_warehouse_id_seq OWNER TO postgres;

--
-- Name: amazon_warehouse_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.amazon_warehouse_id_seq OWNED BY public.amazon_warehouse.id;


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO postgres;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_groups (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO postgres;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_user_permissions (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO postgres;

--
-- Name: amazon_cart id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.amazon_cart ALTER COLUMN id SET DEFAULT nextval('public.amazon_cart_id_seq'::regclass);


--
-- Name: amazon_cartproduct id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.amazon_cartproduct ALTER COLUMN id SET DEFAULT nextval('public.amazon_cartproduct_id_seq'::regclass);


--
-- Name: amazon_category id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.amazon_category ALTER COLUMN id SET DEFAULT nextval('public.amazon_category_id_seq'::regclass);


--
-- Name: amazon_customer id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.amazon_customer ALTER COLUMN id SET DEFAULT nextval('public.amazon_customer_id_seq'::regclass);


--
-- Name: amazon_order id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.amazon_order ALTER COLUMN id SET DEFAULT nextval('public.amazon_order_id_seq'::regclass);


--
-- Name: amazon_orderproduct id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.amazon_orderproduct ALTER COLUMN id SET DEFAULT nextval('public.amazon_orderproduct_id_seq'::regclass);


--
-- Name: amazon_product id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.amazon_product ALTER COLUMN id SET DEFAULT nextval('public.amazon_product_id_seq'::regclass);


--
-- Name: amazon_warehouse id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.amazon_warehouse ALTER COLUMN id SET DEFAULT nextval('public.amazon_warehouse_id_seq'::regclass);


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);


--
-- Name: auth_user_groups id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);


--
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Data for Name: amazon_cart; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.amazon_cart (id, user_id) FROM stdin;
5	3
102	2
\.


--
-- Data for Name: amazon_cartproduct; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.amazon_cartproduct (id, count, cart_id, product_id) FROM stdin;
17	1	5	22
117	1	102	22
118	1	102	23
119	1	102	24
120	2	102	25
\.


--
-- Data for Name: amazon_category; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.amazon_category (id, cat_name, description) FROM stdin;
4	kitchen	Good Kitchen
3	bed	Good Beds
2	desk	Good Desk made in china
1	sofa	as
5	bathroom	Greate bedroom design
6	desk	Greate Desk
\.


--
-- Data for Name: amazon_customer; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.amazon_customer (id, phone, address, state, country, user_id, ups_name) FROM stdin;
2	9198807766	1242 Legacy Terrace	North Carolina	United States	3	\N
3	\N	\N	\N	\N	4	\N
1	91988077612	1242 Legacy Terrace	North Carolina	United States	2	\N
6	9843770804	972	NC	United States	6	\N
4	123123	1242 Legacy Terrace df	North Carolina	United States	5	\N
\.


--
-- Data for Name: amazon_order; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.amazon_order (id, status, ups_name, shipid_or_packageid, truck_id, dest_x, dest_y, created_at, packed_at, loaded_at, delievered_at, user_id, warehouse_id) FROM stdin;
139	purchasing	\N	1539414136226989179	\N	1	2	2022-04-19 19:45:58.213289+00	\N	\N	\N	6	1
132	initialized	\N	2133851800563188859	\N	1	2	2022-04-19 04:09:09.500399+00	\N	\N	\N	6	1
133	initialized	\N	2693708475588248699	\N	1	2	2022-04-19 04:10:01.64179+00	\N	\N	\N	6	1
8	initialized	\N	546938195882280059	\N	1	2	2022-04-17 22:45:45.509128+00	\N	\N	\N	3	1
9	initialized	\N	3517422966041117819	\N	1	2	2022-04-18 01:56:29.083195+00	\N	\N	\N	3	1
10	initialized	\N	1174233648525689979	\N	1	2	2022-04-18 02:14:19.345156+00	\N	\N	\N	3	1
11	initialized	\N	1217611050836345979	\N	1	2	2022-04-18 04:43:41.309118+00	\N	\N	\N	4	1
13	initialized	\N	1996381659185857659	\N	1	2	2022-04-19 01:52:56.265025+00	\N	\N	\N	1	1
14	initialized	\N	2309307575451042939	\N	1	2	2022-04-19 01:53:25.400287+00	\N	\N	\N	1	1
15	initialized	\N	1797856549799003259	\N	1	2	2022-04-19 01:59:47.273183+00	\N	\N	\N	4	1
16	initialized	\N	3844813350762546299	\N	1	2	2022-04-19 02:17:16.928529+00	\N	\N	\N	1	1
49	initialized	\N	2035052649218425979	\N	1	2	2022-04-19 02:21:37.851026+00	\N	\N	\N	1	1
82	initialized	\N	980293328683877499	\N	1	2	2022-04-19 03:02:56.596623+00	\N	\N	\N	6	1
83	initialized	\N	4366343904449217659	\N	1	2	2022-04-19 03:08:11.945897+00	\N	\N	\N	6	1
84	initialized	\N	1368570241384416379	\N	1	2	2022-04-19 03:10:42.252976+00	\N	\N	\N	6	1
85	initialized	\N	2547305493725152379	\N	1	2	2022-04-19 03:12:32.029851+00	\N	\N	\N	6	1
86	initialized	\N	3623246641628415099	\N	1	2	2022-04-19 03:14:12.236893+00	\N	\N	\N	6	1
87	initialized	\N	4459126272616006779	\N	1	2	2022-04-19 03:15:30.082026+00	\N	\N	\N	6	1
88	initialized	\N	949334461385000059	\N	1	2	2022-04-19 03:17:12.703027+00	\N	\N	\N	6	1
89	initialized	\N	2777515004203877499	\N	1	2	2022-04-19 03:20:02.970068+00	\N	\N	\N	6	1
90	initialized	\N	4108110035159336059	\N	1	2	2022-04-19 03:22:06.886951+00	\N	\N	\N	6	1
91	initialized	\N	451274037807809659	\N	1	2	2022-04-19 03:23:35.820284+00	\N	\N	\N	6	1
92	initialized	\N	901902833285334139	\N	1	2	2022-04-19 03:24:17.788758+00	\N	\N	\N	6	1
93	initialized	\N	2111497344043467899	\N	1	2	2022-04-19 03:33:19.934093+00	\N	\N	\N	6	1
94	initialized	\N	3867499221991310459	\N	1	2	2022-04-19 03:36:03.476211+00	\N	\N	\N	6	1
126	initialized	\N	4414245889449952379	\N	1	2	2022-04-19 03:44:03.892563+00	\N	\N	\N	6	1
127	initialized	\N	584308697738822779	\N	1	2	2022-04-19 03:45:16.695877+00	\N	\N	\N	6	1
128	initialized	\N	1737312242663474299	\N	1	2	2022-04-19 03:47:04.077519+00	\N	\N	\N	6	1
129	initialized	\N	2574858320961913979	\N	1	2	2022-04-19 03:48:22.08022+00	\N	\N	\N	6	1
134	initialized	\N	3789082063435826299	\N	1	2	2022-04-19 04:11:43.653798+00	\N	\N	\N	6	1
135	initialized	\N	574731109647369339	\N	1	2	2022-04-19 04:13:53.812927+00	\N	\N	\N	6	1
140	purchasing	\N	2577739531055154299	\N	1	2	2022-04-19 19:47:34.911614+00	\N	\N	\N	6	1
12	cancelled	\N	950496331639899259	\N	1	2	2022-04-20 20:31:50.867415+00	\N	\N	\N	1	1
136	packing	\N	1211385439909692539	\N	1	2	2022-04-19 04:14:53.082328+00	\N	\N	\N	6	1
130	packing	\N	3539028549919097979	\N	1	2	2022-04-19 03:49:51.875742+00	\N	\N	\N	6	1
131	delivering	\N	649737825799177339	1	1	2	2022-04-19 03:52:32.286298+00	\N	\N	\N	6	1
137	purchasing	\N	3098070236235416699	\N	1	2	2022-04-19 19:34:04.375887+00	\N	\N	\N	6	1
138	purchasing	\N	2236147130450707579	\N	1	2	2022-04-19 19:39:53.600677+00	\N	\N	\N	6	1
7	packing	\N	1948669208940676219	\N	1	2	2022-04-17 22:04:59.126605+00	\N	\N	\N	2	1
\.


--
-- Data for Name: amazon_orderproduct; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.amazon_orderproduct (id, count, order_id, product_id) FROM stdin;
1	1	7	23
2	6	7	22
3	1	8	22
4	1	8	23
5	1	9	22
6	2	11	22
7	2	11	23
8	2	12	23
9	1	12	22
10	1	13	25
11	1	14	25
12	1	15	24
13	1	16	25
46	1	49	25
79	1	82	22
80	1	82	23
81	1	83	22
82	1	84	22
83	1	85	22
84	1	86	22
85	1	87	22
86	1	88	22
87	1	89	22
88	1	90	22
89	1	91	22
90	1	92	22
91	1	93	22
92	1	94	22
124	1	126	22
125	1	127	22
126	1	128	22
127	1	129	22
128	1	130	22
129	1	131	22
130	1	132	22
131	1	133	23
132	1	134	22
133	1	135	22
134	1	136	23
135	1	137	23
136	1	137	22
137	1	138	22
138	1	139	22
139	1	140	22
\.


--
-- Data for Name: amazon_product; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.amazon_product (id, name, price, description, photo, category_id) FROM stdin;
22	Chair 1	123	Good Chairs with fair price	product-1.png	1
23	Chair 2	234	Good Desk made in china	product-2.png	1
24	Beds	450	Good bed with fair price	product-3.png	3
25	Kitchens from china	3900	Good good good	product-10.png	4
26	Bedroom Greate	500	Great Discount	livingroom-category.jpeg	5
27	Great Desk	400	Made in China	kitchen-category.jpeg	6
28	Desk 2	560	Greate Desk	patio-category.jpeg	6
\.


--
-- Data for Name: amazon_warehouse; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.amazon_warehouse (id, x, y) FROM stdin;
1	1	2
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add permission	1	add_permission
2	Can change permission	1	change_permission
3	Can delete permission	1	delete_permission
4	Can view permission	1	view_permission
5	Can add group	2	add_group
6	Can change group	2	change_group
7	Can delete group	2	delete_group
8	Can view group	2	view_group
9	Can add user	3	add_user
10	Can change user	3	change_user
11	Can delete user	3	delete_user
12	Can view user	3	view_user
13	Can add content type	4	add_contenttype
14	Can change content type	4	change_contenttype
15	Can delete content type	4	delete_contenttype
16	Can view content type	4	view_contenttype
17	Can add cart	5	add_cart
18	Can change cart	5	change_cart
19	Can delete cart	5	delete_cart
20	Can view cart	5	view_cart
21	Can add category	6	add_category
22	Can change category	6	change_category
23	Can delete category	6	delete_category
24	Can view category	6	view_category
25	Can add customer	7	add_customer
26	Can change customer	7	change_customer
27	Can delete customer	7	delete_customer
28	Can view customer	7	view_customer
29	Can add order	8	add_order
30	Can change order	8	change_order
31	Can delete order	8	delete_order
32	Can view order	8	view_order
33	Can add warehouse	9	add_warehouse
34	Can change warehouse	9	change_warehouse
35	Can delete warehouse	9	delete_warehouse
36	Can view warehouse	9	view_warehouse
37	Can add product	10	add_product
38	Can change product	10	change_product
39	Can delete product	10	delete_product
40	Can view product	10	view_product
41	Can add order product	11	add_orderproduct
42	Can change order product	11	change_orderproduct
43	Can delete order product	11	delete_orderproduct
44	Can view order product	11	view_orderproduct
45	Can add cart product	12	add_cartproduct
46	Can change cart product	12	change_cartproduct
47	Can delete cart product	12	delete_cartproduct
48	Can view cart product	12	view_cartproduct
49	Can add log entry	13	add_logentry
50	Can change log entry	13	change_logentry
51	Can delete log entry	13	delete_logentry
52	Can view log entry	13	view_logentry
53	Can add session	14	add_session
54	Can change session	14	change_session
55	Can delete session	14	delete_session
56	Can view session	14	view_session
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
4	pbkdf2_sha256$320000$crEZ23YsubFlW2wrhfJ5UT$yCSrvhlTwcdVu3Wlb0NGmcygpB0f9QybRknW02ISUNA=	2022-04-17 22:45:09.779391+00	f	wanglun			l23@duke.edu	f	t	2022-04-17 22:45:09.464622+00
5	pbkdf2_sha256$320000$DGiGoN5JGHubvFpsK57nLz$8utw5tU+s8gjEacFAxYlsOuy1T2iSl/9chhQFQmDDqA=	2022-04-18 04:30:24.570932+00	f	www			lw32@duke.edu	f	t	2022-04-18 02:56:27.353607+00
6	pbkdf2_sha256$320000$n35lLFWwmPNDMeM9O3OtTX$AYSlgM9evpj/H/bVpQ1H3EsnBqz93+OirI2E4Tp0q+0=	2022-04-19 03:00:26.80039+00	f	ct265			ct265@duke.edu	f	t	2022-04-19 03:00:26.537489+00
3	pbkdf2_sha256$320000$AEE73pgkXibyBTy6RJw9fb$kpVTolSbm5nRRHoH5YNieO/EqRH4iyYAFBnybqDMvo8=	2022-04-20 21:09:58.526973+00	f	calmanddown			lun.wang@duke.edu	f	t	2022-04-17 01:37:22.846166+00
2	pbkdf2_sha256$320000$mbMRoFjhZEJG1zCDCimVFz$PmZua70rRHoube06c+sQeYtqjvS7GjohB5EcZPpSQsE=	2022-04-21 00:39:38.091864+00	t	root				t	t	2022-04-16 18:25:06.566377+00
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2022-04-16 18:25:29.015382+00	1	Customer object (1)	1	[{"added": {}}]	7	2
2	2022-04-16 18:25:35.775647+00	1	Warehouse object (1)	1	[{"added": {}}]	9	2
3	2022-04-16 18:27:38.777627+00	1	Order object (1)	1	[{"added": {}}]	8	2
4	2022-04-16 18:27:41.965245+00	2	Order object (2)	1	[{"added": {}}]	8	2
5	2022-04-16 18:27:45.131111+00	3	Order object (3)	1	[{"added": {}}]	8	2
6	2022-04-16 18:28:58.314566+00	4	Order object (4)	1	[{"added": {}}]	8	2
7	2022-04-16 18:29:43.30235+00	5	Order object (5)	1	[{"added": {}}]	8	2
8	2022-04-16 18:29:59.283633+00	6	Order object (6)	1	[{"added": {}}]	8	2
9	2022-04-16 19:04:41.300591+00	1	Category object (1)	1	[{"added": {}}]	6	2
10	2022-04-16 19:04:42.979887+00	1	Product object (1)	1	[{"added": {}}]	10	2
11	2022-04-16 19:10:48.902709+00	2	Product object (2)	1	[{"added": {}}]	10	2
12	2022-04-16 19:21:11.685628+00	3	Product object (3)	1	[{"added": {}}]	10	2
13	2022-04-16 19:45:47.928613+00	4	Product object (4)	1	[{"added": {}}]	10	2
14	2022-04-16 21:31:32.708956+00	3	Product object (3)	3		10	2
15	2022-04-16 21:31:37.382851+00	2	Product object (2)	3		10	2
16	2022-04-16 21:31:40.919358+00	1	Product object (1)	3		10	2
17	2022-04-16 21:32:02.172205+00	5	Product object (5)	1	[{"added": {}}]	10	2
18	2022-04-16 21:32:44.958502+00	6	Product object (6)	1	[{"added": {}}]	10	2
19	2022-04-16 22:22:56.116473+00	6	Product object (6)	3		10	2
20	2022-04-16 22:23:00.30044+00	5	Product object (5)	3		10	2
21	2022-04-16 22:23:03.401177+00	4	Product object (4)	3		10	2
22	2022-04-16 22:25:18.320905+00	7	Product object (7)	1	[{"added": {}}]	10	2
23	2022-04-16 22:25:34.76362+00	8	Product object (8)	1	[{"added": {}}]	10	2
24	2022-04-16 22:26:17.109992+00	2	Category object (2)	1	[{"added": {}}]	6	2
25	2022-04-16 22:26:18.959236+00	9	Product object (9)	1	[{"added": {}}]	10	2
26	2022-04-16 22:27:47.698372+00	8	Product object (8)	3		10	2
27	2022-04-16 22:27:52.72837+00	9	Product object (9)	3		10	2
28	2022-04-16 22:27:55.949424+00	7	Product object (7)	3		10	2
29	2022-04-16 22:28:15.3314+00	10	Product object (10)	1	[{"added": {}}]	10	2
30	2022-04-17 04:09:28.880957+00	11	Product object (11)	1	[{"added": {}}]	10	2
31	2022-04-17 04:13:59.158512+00	12	Product object (12)	1	[{"added": {}}]	10	2
32	2022-04-17 04:20:45.613575+00	10	Product object (10)	3		10	2
33	2022-04-17 04:20:49.725814+00	12	Product object (12)	3		10	2
34	2022-04-17 04:21:05.17524+00	13	Product object (13)	1	[{"added": {}}]	10	2
35	2022-04-17 04:23:51.02162+00	13	Product object (13)	3		10	2
36	2022-04-17 04:23:54.544146+00	11	Product object (11)	3		10	2
37	2022-04-17 04:24:35.207383+00	14	Product object (14)	1	[{"added": {}}]	10	2
38	2022-04-17 04:27:33.55235+00	15	Product object (15)	1	[{"added": {}}]	10	2
39	2022-04-17 04:32:03.225295+00	15	Product object (15)	3		10	2
40	2022-04-17 04:32:07.557574+00	14	Product object (14)	3		10	2
41	2022-04-17 04:32:50.684072+00	16	Product object (16)	1	[{"added": {}}]	10	2
42	2022-04-17 04:33:41.28248+00	16	Product object (16)	3		10	2
43	2022-04-17 04:34:09.976539+00	17	Product object (17)	1	[{"added": {}}]	10	2
44	2022-04-17 04:35:23.087869+00	18	Product object (18)	1	[{"added": {}}]	10	2
45	2022-04-17 04:36:45.282137+00	19	Product object (19)	1	[{"added": {}}]	10	2
46	2022-04-17 04:43:30.271493+00	20	Product object (20)	1	[{"added": {}}]	10	2
47	2022-04-17 05:05:08.278879+00	17	Product object (17)	3		10	2
48	2022-04-17 05:05:11.726783+00	18	Product object (18)	3		10	2
49	2022-04-17 05:05:15.252879+00	19	Product object (19)	3		10	2
50	2022-04-17 05:10:00.402001+00	20	Product object (20)	3		10	2
51	2022-04-17 05:10:11.374415+00	21	Product object (21)	1	[{"added": {}}]	10	2
52	2022-04-17 05:10:24.872639+00	21	Product object (21)	3		10	2
53	2022-04-17 05:10:44.361994+00	22	Product object (22)	1	[{"added": {}}]	10	2
54	2022-04-17 05:13:58.881795+00	23	Product object (23)	1	[{"added": {}}]	10	2
55	2022-04-17 22:43:55.325103+00	6	Order object (6)	3		8	2
56	2022-04-17 22:44:00.394375+00	5	Order object (5)	3		8	2
57	2022-04-17 22:44:04.604958+00	4	Order object (4)	3		8	2
58	2022-04-17 22:44:08.397485+00	3	Order object (3)	3		8	2
59	2022-04-17 22:44:12.496708+00	2	Order object (2)	3		8	2
60	2022-04-17 22:44:16.279623+00	1	Order object (1)	3		8	2
61	2022-04-18 03:42:35.747849+00	3	Category object (3)	1	[{"added": {}}]	6	2
62	2022-04-18 03:42:37.264388+00	24	Product object (24)	1	[{"added": {}}]	10	2
63	2022-04-18 16:32:33.794246+00	4	Category object (4)	1	[{"added": {}}]	6	2
64	2022-04-18 16:33:07.399379+00	25	Product object (25)	1	[{"added": {}}]	10	2
65	2022-04-18 17:09:39.200797+00	3	Category object (3)	2	[{"changed": {"fields": ["Cat name"]}}]	6	2
66	2022-04-18 17:09:44.543001+00	2	Category object (2)	2	[{"changed": {"fields": ["Cat name"]}}]	6	2
67	2022-04-18 17:09:50.604391+00	1	Category object (1)	2	[{"changed": {"fields": ["Cat name"]}}]	6	2
68	2022-04-21 00:41:55.239756+00	5	Category object (5)	1	[{"added": {}}]	6	2
69	2022-04-21 00:41:57.035517+00	26	Product object (26)	1	[{"added": {}}]	10	2
70	2022-04-21 00:46:38.503663+00	5	Category object (5)	2	[{"changed": {"fields": ["Cat name"]}}]	6	2
71	2022-04-21 00:47:33.293372+00	6	Category object (6)	1	[{"added": {}}]	6	2
72	2022-04-21 00:47:34.929146+00	27	Product object (27)	1	[{"added": {}}]	10	2
73	2022-04-21 00:48:14.605197+00	28	Product object (28)	1	[{"added": {}}]	10	2
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	auth	permission
2	auth	group
3	auth	user
4	contenttypes	contenttype
5	amazon	cart
6	amazon	category
7	amazon	customer
8	amazon	order
9	amazon	warehouse
10	amazon	product
11	amazon	orderproduct
12	amazon	cartproduct
13	admin	logentry
14	sessions	session
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2022-04-16 18:19:40.94259+00
2	auth	0001_initial	2022-04-16 18:19:41.038381+00
3	amazon	0001_initial	2022-04-16 18:19:41.181304+00
4	amazon	0002_alter_order_shipid_or_packageid	2022-04-16 18:24:19.327965+00
5	admin	0001_initial	2022-04-16 18:24:54.429344+00
6	admin	0002_logentry_remove_auto_add	2022-04-16 18:24:54.439079+00
7	admin	0003_logentry_add_action_flag_choices	2022-04-16 18:24:54.448884+00
8	contenttypes	0002_remove_content_type_name	2022-04-16 18:24:54.474323+00
9	auth	0002_alter_permission_name_max_length	2022-04-16 18:24:54.489996+00
10	auth	0003_alter_user_email_max_length	2022-04-16 18:24:54.501359+00
11	auth	0004_alter_user_username_opts	2022-04-16 18:24:54.513563+00
12	auth	0005_alter_user_last_login_null	2022-04-16 18:24:54.525724+00
13	auth	0006_require_contenttypes_0002	2022-04-16 18:24:54.530964+00
14	auth	0007_alter_validators_add_error_messages	2022-04-16 18:24:54.540717+00
15	auth	0008_alter_user_username_max_length	2022-04-16 18:24:54.554918+00
16	auth	0009_alter_user_last_name_max_length	2022-04-16 18:24:54.565977+00
17	auth	0010_alter_group_name_max_length	2022-04-16 18:24:54.584201+00
18	auth	0011_update_proxy_permissions	2022-04-16 18:24:54.597619+00
19	auth	0012_alter_user_first_name_max_length	2022-04-16 18:24:54.60741+00
20	sessions	0001_initial	2022-04-16 18:24:54.620233+00
21	amazon	0003_rename_dext_y_order_dest_y_alter_cartproduct_cart_id_and_more	2022-04-16 19:04:06.812077+00
22	amazon	0004_alter_product_photo	2022-04-16 19:10:19.670498+00
23	amazon	0005_alter_product_photo	2022-04-16 19:20:43.294276+00
24	amazon	0006_alter_product_photo	2022-04-16 19:36:43.707162+00
25	amazon	0007_alter_product_photo	2022-04-16 21:32:30.702949+00
26	amazon	0008_alter_product_photo	2022-04-16 22:27:33.910566+00
27	amazon	0009_alter_cartproduct_count	2022-04-17 02:42:16.744326+00
28	amazon	0010_alter_cart_user_id	2022-04-17 02:57:33.054125+00
29	amazon	0011_alter_customer_user	2022-04-17 03:07:08.912754+00
30	amazon	0002_alter_order_status	2022-04-18 05:05:36.680252+00
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
6qqo0iv6afrtlnutw4jcvakwrjg6zs7w	.eJxVjM0OwiAQhN-FsyHLz1bw6N1nIAsLUjU0Ke3J-O62SQ96m8z3zbxFoHWpYe15DiOLi0Bx-u0ipWduO-AHtfsk09SWeYxyV-RBu7xNnF_Xw_07qNTrtrZUDDufrDJIHnDwJSY03qqC-TwAFwUGXEzg1JZIJ7RMmsFBcc5o8fkCz903BQ:1ngIWv:E4Gu3T1RVY594qSbH2l4kCGqTfcU8_tnKJKGFiEqEYw	2022-05-02 03:58:25.901334+00
n5ot6ssfzj9nx0mwlhb5a1a78iw8p8vc	.eJxVjM0OwiAQhN-FsyHLz1bw6N1nIAsLUjU0Ke3J-O62SQ96m8z3zbxFoHWpYe15DiOLi0Bx-u0ipWduO-AHtfsk09SWeYxyV-RBu7xNnF_Xw_07qNTrtrZUDDufrDJIHnDwJSY03qqC-TwAFwUGXEzg1JZIJ7RMmsFBcc5o8fkCz903BQ:1ngJ1s:Tban95dVFrXX9UKW5VyCPXblv7YeXkYk7DaYxfEfYF0	2022-05-02 04:30:24.575665+00
do57zavonmpgam3z85lioy6gvo6fnyd4	.eJxVjEsOwiAYBu_C2hDeiEv3PQPh50OpGpqUdmW8uyHpQrczk3mzmPatxr2XNc5gF-bY6ZdRys_ShsAjtfvC89K2dSY-En7YzqcF5XU92r9BTb2OrQxJwntjoMnBS-TggihI3iilb5ZUVmenCQQbQM4qCx2EksLDZcE-X9oKN3I:1nge6M:HraE1pUMsDgpTLd1QyB5D_g8SgBOpsMM7RKclyiooJc	2022-05-03 03:00:26.81597+00
a63vkff302po3bq2ciudcs7dqcxoplb9	.eJxVjDsOwjAQBe_iGlle_-JQ0nMGa9dr4wBypDipEHeHSCmgfTPzXiLitta49bzEicVZaHH63QjTI7cd8B3bbZZpbusykdwVedAurzPn5-Vw_w4q9vqtyQUEw5yIbFLaA4WA1gxkXCrBaLbswY2OS85jYTCghuAUFOUZWJF4fwDwBTfw:1nhKrC:blv7zj07aOvRUSY9mR9uuLms1cNOVFKknKHU00KyY_I	2022-05-05 00:39:38.128908+00
\.


--
-- Name: amazon_cart_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.amazon_cart_id_seq', 102, true);


--
-- Name: amazon_cartproduct_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.amazon_cartproduct_id_seq', 120, true);


--
-- Name: amazon_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.amazon_category_id_seq', 6, true);


--
-- Name: amazon_customer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.amazon_customer_id_seq', 6, true);


--
-- Name: amazon_order_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.amazon_order_id_seq', 140, true);


--
-- Name: amazon_orderproduct_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.amazon_orderproduct_id_seq', 139, true);


--
-- Name: amazon_product_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.amazon_product_id_seq', 28, true);


--
-- Name: amazon_warehouse_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.amazon_warehouse_id_seq', 1, true);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 56, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 6, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 73, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 14, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 30, true);


--
-- Name: amazon_cart amazon_cart_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.amazon_cart
    ADD CONSTRAINT amazon_cart_pkey PRIMARY KEY (id);


--
-- Name: amazon_cartproduct amazon_cartproduct_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.amazon_cartproduct
    ADD CONSTRAINT amazon_cartproduct_pkey PRIMARY KEY (id);


--
-- Name: amazon_category amazon_category_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.amazon_category
    ADD CONSTRAINT amazon_category_pkey PRIMARY KEY (id);


--
-- Name: amazon_customer amazon_customer_phone_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.amazon_customer
    ADD CONSTRAINT amazon_customer_phone_key UNIQUE (phone);


--
-- Name: amazon_customer amazon_customer_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.amazon_customer
    ADD CONSTRAINT amazon_customer_pkey PRIMARY KEY (id);


--
-- Name: amazon_customer amazon_customer_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.amazon_customer
    ADD CONSTRAINT amazon_customer_user_id_key UNIQUE (user_id);


--
-- Name: amazon_order amazon_order_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.amazon_order
    ADD CONSTRAINT amazon_order_pkey PRIMARY KEY (id);


--
-- Name: amazon_orderproduct amazon_orderproduct_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.amazon_orderproduct
    ADD CONSTRAINT amazon_orderproduct_pkey PRIMARY KEY (id);


--
-- Name: amazon_product amazon_product_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.amazon_product
    ADD CONSTRAINT amazon_product_pkey PRIMARY KEY (id);


--
-- Name: amazon_warehouse amazon_warehouse_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.amazon_warehouse
    ADD CONSTRAINT amazon_warehouse_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: amazon_cart_user_id_id_11aea1a3; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX amazon_cart_user_id_id_11aea1a3 ON public.amazon_cart USING btree (user_id);


--
-- Name: amazon_cartproduct_cart_id_id_c5f0e954; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX amazon_cartproduct_cart_id_id_c5f0e954 ON public.amazon_cartproduct USING btree (cart_id);


--
-- Name: amazon_cartproduct_product_id_id_105ddb12; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX amazon_cartproduct_product_id_id_105ddb12 ON public.amazon_cartproduct USING btree (product_id);


--
-- Name: amazon_customer_phone_f1bad36b_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX amazon_customer_phone_f1bad36b_like ON public.amazon_customer USING btree (phone varchar_pattern_ops);


--
-- Name: amazon_order_user_id_id_d302e2ad; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX amazon_order_user_id_id_d302e2ad ON public.amazon_order USING btree (user_id);


--
-- Name: amazon_order_warehouse_id_id_3d791e30; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX amazon_order_warehouse_id_id_3d791e30 ON public.amazon_order USING btree (warehouse_id);


--
-- Name: amazon_orderproduct_order_id_id_50beaaa7; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX amazon_orderproduct_order_id_id_50beaaa7 ON public.amazon_orderproduct USING btree (order_id);


--
-- Name: amazon_orderproduct_product_id_id_cee50fda; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX amazon_orderproduct_product_id_id_cee50fda ON public.amazon_orderproduct USING btree (product_id);


--
-- Name: amazon_product_category_id_id_1e7dea24; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX amazon_product_category_id_id_1e7dea24 ON public.amazon_product USING btree (category_id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: amazon_cart amazon_cart_user_id_1e2131b5_fk_amazon_customer_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.amazon_cart
    ADD CONSTRAINT amazon_cart_user_id_1e2131b5_fk_amazon_customer_id FOREIGN KEY (user_id) REFERENCES public.amazon_customer(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: amazon_cartproduct amazon_cartproduct_cart_id_dea62536_fk_amazon_cart_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.amazon_cartproduct
    ADD CONSTRAINT amazon_cartproduct_cart_id_dea62536_fk_amazon_cart_id FOREIGN KEY (cart_id) REFERENCES public.amazon_cart(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: amazon_cartproduct amazon_cartproduct_product_id_f314d1b5_fk_amazon_product_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.amazon_cartproduct
    ADD CONSTRAINT amazon_cartproduct_product_id_f314d1b5_fk_amazon_product_id FOREIGN KEY (product_id) REFERENCES public.amazon_product(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: amazon_customer amazon_customer_user_id_81eb9a17_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.amazon_customer
    ADD CONSTRAINT amazon_customer_user_id_81eb9a17_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: amazon_order amazon_order_user_id_82fd3472_fk_amazon_customer_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.amazon_order
    ADD CONSTRAINT amazon_order_user_id_82fd3472_fk_amazon_customer_id FOREIGN KEY (user_id) REFERENCES public.amazon_customer(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: amazon_order amazon_order_warehouse_id_54803e63_fk_amazon_warehouse_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.amazon_order
    ADD CONSTRAINT amazon_order_warehouse_id_54803e63_fk_amazon_warehouse_id FOREIGN KEY (warehouse_id) REFERENCES public.amazon_warehouse(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: amazon_orderproduct amazon_orderproduct_order_id_21b2132c_fk_amazon_order_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.amazon_orderproduct
    ADD CONSTRAINT amazon_orderproduct_order_id_21b2132c_fk_amazon_order_id FOREIGN KEY (order_id) REFERENCES public.amazon_order(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: amazon_orderproduct amazon_orderproduct_product_id_e4d534e9_fk_amazon_product_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.amazon_orderproduct
    ADD CONSTRAINT amazon_orderproduct_product_id_e4d534e9_fk_amazon_product_id FOREIGN KEY (product_id) REFERENCES public.amazon_product(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: amazon_product amazon_product_category_id_9ad4156b_fk_amazon_category_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.amazon_product
    ADD CONSTRAINT amazon_product_category_id_9ad4156b_fk_amazon_category_id FOREIGN KEY (category_id) REFERENCES public.amazon_category(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--


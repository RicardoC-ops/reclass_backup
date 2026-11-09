SET session_replication_role = replica;

--
-- PostgreSQL database dump
--

-- \restrict yze87rSzXgt6w4CclDhXGXnm0e4AT3QnIedoiOSH2WbNcT7W1AzlBrOaKWOcVs4

-- Dumped from database version 17.11
-- Dumped by pg_dump version 17.11

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: audit_log_entries; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."audit_log_entries" ("instance_id", "id", "payload", "created_at", "ip_address") FROM stdin;
\.


--
-- Data for Name: custom_oauth_providers; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."custom_oauth_providers" ("id", "provider_type", "identifier", "name", "client_id", "client_secret", "acceptable_client_ids", "scopes", "pkce_enabled", "attribute_mapping", "authorization_params", "enabled", "email_optional", "issuer", "discovery_url", "skip_nonce_check", "cached_discovery", "discovery_cached_at", "authorization_url", "token_url", "userinfo_url", "jwks_uri", "created_at", "updated_at", "custom_claims_allowlist") FROM stdin;
\.


--
-- Data for Name: flow_state; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."flow_state" ("id", "user_id", "auth_code", "code_challenge_method", "code_challenge", "provider_type", "provider_access_token", "provider_refresh_token", "created_at", "updated_at", "authentication_method", "auth_code_issued_at", "invite_token", "referrer", "oauth_client_state_id", "linking_target_id", "email_optional") FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."users" ("instance_id", "id", "aud", "role", "email", "encrypted_password", "email_confirmed_at", "invited_at", "confirmation_token", "confirmation_sent_at", "recovery_token", "recovery_sent_at", "email_change_token_new", "email_change", "email_change_sent_at", "last_sign_in_at", "raw_app_meta_data", "raw_user_meta_data", "is_super_admin", "created_at", "updated_at", "phone", "phone_confirmed_at", "phone_change", "phone_change_token", "phone_change_sent_at", "email_change_token_current", "email_change_confirm_status", "banned_until", "reauthentication_token", "reauthentication_sent_at", "is_sso_user", "deleted_at", "is_anonymous") FROM stdin;
00000000-0000-0000-0000-000000000000	fb4d031e-3db9-40e3-9df8-d26e0dea6d34	authenticated	authenticated	enzoecassio1info@gmail.com	$2a$10$4a0jeoVtIRLUwdr.HwDQle9sJ15E0WP6bxqALLWaOrSellceFEgoS	2026-10-28 15:53:38.384563+00	\N		\N		\N			\N	2026-10-28 16:13:19.807303+00	{"provider": "email", "providers": ["email"]}	{"nome": "enzo", "email_verified": true}	\N	2026-10-28 15:53:38.373591+00	2026-10-28 16:13:19.822608+00	\N	\N			\N		0	\N		\N	f	\N	f
00000000-0000-0000-0000-000000000000	b2af0b84-dd5c-474f-9614-fe3a3683421c	authenticated	authenticated	enzoecassio2@gmail.com	$2a$10$bWry2iJ2P2QdahlnkE2n9ePgrJbNJC.6BzQVW1nL1VDQ3Nt8gX7Pq	2026-10-28 15:39:24.699361+00	\N		\N		\N			\N	2026-10-28 16:13:47.29252+00	{"provider": "email", "providers": ["email"]}	{"sub": "b2af0b84-dd5c-474f-9614-fe3a3683421c", "nome": "enzo", "email": "enzoecassio2@gmail.com", "email_verified": true, "phone_verified": false}	\N	2026-10-28 15:39:24.694405+00	2026-10-28 16:13:47.298915+00	\N	\N			\N		0	\N		\N	f	\N	f
\.


--
-- Data for Name: identities; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."identities" ("provider_id", "user_id", "identity_data", "provider", "last_sign_in_at", "created_at", "updated_at", "id") FROM stdin;
b2af0b84-dd5c-474f-9614-fe3a3683421c	b2af0b84-dd5c-474f-9614-fe3a3683421c	{"sub": "b2af0b84-dd5c-474f-9614-fe3a3683421c", "nome": "enzo", "email": "enzoecassio2@gmail.com", "email_verified": false, "phone_verified": false}	email	2026-10-28 15:39:24.697131+00	2026-10-28 15:39:24.697174+00	2026-10-28 15:39:24.697174+00	1382aca4-1496-4ab4-925e-cd7a0fe31b81
fb4d031e-3db9-40e3-9df8-d26e0dea6d34	fb4d031e-3db9-40e3-9df8-d26e0dea6d34	{"sub": "fb4d031e-3db9-40e3-9df8-d26e0dea6d34", "email": "enzoecassio1info@gmail.com", "email_verified": false, "phone_verified": false}	email	2026-10-28 15:53:38.382364+00	2026-10-28 15:53:38.382421+00	2026-10-28 15:53:38.382421+00	94f136f1-f284-4d1a-8f30-d86da9045681
\.


--
-- Data for Name: instances; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."instances" ("id", "uuid", "raw_base_config", "created_at", "updated_at") FROM stdin;
\.


--
-- Data for Name: oauth_clients; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."oauth_clients" ("id", "client_secret_hash", "registration_type", "redirect_uris", "grant_types", "client_name", "client_uri", "logo_uri", "created_at", "updated_at", "deleted_at", "client_type", "token_endpoint_auth_method") FROM stdin;
\.


--
-- Data for Name: sessions; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."sessions" ("id", "user_id", "created_at", "updated_at", "factor_id", "aal", "not_after", "refreshed_at", "user_agent", "ip", "tag", "oauth_client_id", "refresh_token_hmac_key", "refresh_token_counter", "scopes") FROM stdin;
\.


--
-- Data for Name: mfa_amr_claims; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."mfa_amr_claims" ("session_id", "created_at", "updated_at", "authentication_method", "id") FROM stdin;
\.


--
-- Data for Name: mfa_factors; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."mfa_factors" ("id", "user_id", "friendly_name", "factor_type", "status", "created_at", "updated_at", "secret", "phone", "last_challenged_at", "web_authn_credential", "web_authn_aaguid", "last_webauthn_challenge_data") FROM stdin;
\.


--
-- Data for Name: mfa_challenges; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."mfa_challenges" ("id", "factor_id", "created_at", "verified_at", "ip_address", "otp_code", "web_authn_session_data") FROM stdin;
\.


--
-- Data for Name: mfa_recovery_code_sets; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."mfa_recovery_code_sets" ("id", "user_id", "mfa_factor_id", "failed_verification_count", "verification_locked_until", "created_at", "updated_at") FROM stdin;
\.


--
-- Data for Name: mfa_recovery_codes; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."mfa_recovery_codes" ("id", "mfa_recovery_code_set_id", "code_hash", "consumed_at", "created_at") FROM stdin;
\.


--
-- Data for Name: oauth_authorizations; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."oauth_authorizations" ("id", "authorization_id", "client_id", "user_id", "redirect_uri", "scope", "state", "resource", "code_challenge", "code_challenge_method", "response_type", "status", "authorization_code", "created_at", "expires_at", "approved_at", "nonce") FROM stdin;
\.


--
-- Data for Name: oauth_client_states; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."oauth_client_states" ("id", "provider_type", "code_verifier", "created_at") FROM stdin;
\.


--
-- Data for Name: oauth_consents; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."oauth_consents" ("id", "user_id", "client_id", "scopes", "granted_at", "revoked_at") FROM stdin;
\.


--
-- Data for Name: one_time_tokens; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."one_time_tokens" ("id", "user_id", "token_type", "token_hash", "relates_to", "created_at", "updated_at", "expires_at") FROM stdin;
\.


--
-- Data for Name: refresh_tokens; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."refresh_tokens" ("instance_id", "id", "token", "user_id", "revoked", "created_at", "updated_at", "parent", "session_id") FROM stdin;
\.


--
-- Data for Name: sso_providers; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."sso_providers" ("id", "resource_id", "created_at", "updated_at", "disabled") FROM stdin;
\.


--
-- Data for Name: saml_providers; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."saml_providers" ("id", "sso_provider_id", "entity_id", "metadata_xml", "metadata_url", "attribute_mapping", "created_at", "updated_at", "name_id_format") FROM stdin;
\.


--
-- Data for Name: saml_relay_states; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."saml_relay_states" ("id", "sso_provider_id", "request_id", "for_email", "redirect_to", "created_at", "updated_at", "flow_state_id") FROM stdin;
\.


--
-- Data for Name: scim_tokens; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."scim_tokens" ("id", "sso_provider_id", "token_hash", "prefix", "created_at", "expires_at", "revoked_at", "last_used_at") FROM stdin;
\.


--
-- Data for Name: scim_users; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."scim_users" ("id", "sso_provider_id", "user_id", "resource", "created_at", "updated_at", "deleted_at") FROM stdin;
\.


--
-- Data for Name: sso_domains; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."sso_domains" ("id", "sso_provider_id", "domain", "created_at", "updated_at") FROM stdin;
\.


--
-- Data for Name: webauthn_challenges; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."webauthn_challenges" ("id", "user_id", "challenge_type", "session_data", "created_at", "expires_at") FROM stdin;
\.


--
-- Data for Name: webauthn_credentials; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."webauthn_credentials" ("id", "user_id", "credential_id", "public_key", "attestation_type", "aaguid", "sign_count", "transports", "backup_eligible", "backed_up", "friendly_name", "created_at", "updated_at", "last_used_at") FROM stdin;
\.


--
-- Data for Name: profiles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."profiles" ("id", "nome", "tipo_usuario", "created_at", "email", "avatar_url") FROM stdin;
fb4d031e-3db9-40e3-9df8-d26e0dea6d34	enzo	professor	2026-10-28 15:53:38.371333+00	enzoecassio1info@gmail.com	\N
b2af0b84-dd5c-474f-9614-fe3a3683421c	enzo	aluno	2026-10-28 15:39:24.694104+00	enzoecassio2@gmail.com	https://mggntdrbjbojflihpeae.supabase.co/storage/v1/object/public/avatars/b2af0b84-dd5c-474f-9614-fe3a3683421c/5096f49b-b269-4d1c-8ebb-0c494db96910.jpg
\.


--
-- Data for Name: agendamentos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."agendamentos" ("id", "id_aluno", "aula", "data", "horario", "status", "created_at") FROM stdin;
3	b2af0b84-dd5c-474f-9614-fe3a3683421c	Present Perfect (Inglês)	2026-11-15	19:00:00	repor	2026-10-28 16:20:25.109873+00
4	b2af0b84-dd5c-474f-9614-fe3a3683421c	Present Perfect (Inglês)	2026-11-15	19:00:00	repor	2026-10-28 16:31:24.521383+00
\.


--
-- Data for Name: aulas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."aulas" ("id", "titulo", "data", "horario", "unidade", "vagas", "observacoes", "professor_id", "created_at") FROM stdin;
\.


--
-- Data for Name: buckets; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY "storage"."buckets" ("id", "name", "owner", "created_at", "updated_at", "public", "avif_autodetection", "file_size_limit", "allowed_mime_types", "owner_id", "type", "versioning_status", "lifecycle_configuration", "lifecycle_configuration_generation") FROM stdin;
avatars	avatars	\N	2026-10-28 16:23:39.895531+00	2026-10-28 16:23:39.895531+00	t	f	5242880	{image/jpeg,image/png,image/webp}	\N	STANDARD	DISABLED	\N	\N
\.


--
-- Data for Name: buckets_analytics; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY "storage"."buckets_analytics" ("name", "type", "format", "created_at", "updated_at", "id", "deleted_at") FROM stdin;
\.


--
-- Data for Name: buckets_vectors; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY "storage"."buckets_vectors" ("id", "type", "created_at", "updated_at") FROM stdin;
\.


--
-- Data for Name: objects; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY "storage"."objects" ("id", "bucket_id", "name", "owner", "created_at", "updated_at", "last_accessed_at", "metadata", "version", "owner_id", "user_metadata", "archived_at", "is_delete_marker", "is_versioned") FROM stdin;
3db7b498-0ae6-4a7e-99e4-591eb667caf9	avatars	b2af0b84-dd5c-474f-9614-fe3a3683421c/65fe9b85-8f3c-44a8-884b-2cc5c13c5771.jpg	b2af0b84-dd5c-474f-9614-fe3a3683421c	2026-10-28 16:23:55.874445+00	2026-10-28 16:23:55.874445+00	2026-10-28 16:23:55.874445+00	{"eTag": "\\"de946fe039ee64eea1e93d46344ca749\\"", "size": 4258586, "mimetype": "image/jpeg", "cacheControl": "max-age=3600", "lastModified": "2026-10-28T16:23:56.000Z", "contentLength": 4258586, "httpStatusCode": 200}	4d31bc7b-ae6a-4bf1-8d6a-ab0eecb6df24	b2af0b84-dd5c-474f-9614-fe3a3683421c	{}	\N	f	f
e2db185f-b22b-4990-9044-e65a820baeab	avatars	b2af0b84-dd5c-474f-9614-fe3a3683421c/64b40426-e196-477b-aa5b-02e704b107eb.png	b2af0b84-dd5c-474f-9614-fe3a3683421c	2026-10-28 16:24:05.724975+00	2026-10-28 16:24:05.724975+00	2026-10-28 16:24:05.724975+00	{"eTag": "\\"884f34d54d46b1128ed68d5558dd38c3\\"", "size": 1948984, "mimetype": "image/png", "cacheControl": "max-age=3600", "lastModified": "2026-10-28T16:24:06.000Z", "contentLength": 1948984, "httpStatusCode": 200}	0f0b9604-4488-4ff4-8eeb-42baa8c5b9d2	b2af0b84-dd5c-474f-9614-fe3a3683421c	{}	\N	f	f
5365e071-d446-483d-9717-3740000658b3	avatars	b2af0b84-dd5c-474f-9614-fe3a3683421c/5096f49b-b269-4d1c-8ebb-0c494db96910.jpg	b2af0b84-dd5c-474f-9614-fe3a3683421c	2026-10-28 16:26:27.761876+00	2026-10-28 16:26:27.761876+00	2026-10-28 16:26:27.761876+00	{"eTag": "\\"de946fe039ee64eea1e93d46344ca749\\"", "size": 4258586, "mimetype": "image/jpeg", "cacheControl": "max-age=3600", "lastModified": "2026-10-28T16:26:28.000Z", "contentLength": 4258586, "httpStatusCode": 200}	4d8f0349-ba13-4f4b-8f27-33d65ab5e94e	b2af0b84-dd5c-474f-9614-fe3a3683421c	{}	\N	f	f
\.


--
-- Data for Name: s3_multipart_uploads; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY "storage"."s3_multipart_uploads" ("id", "in_progress_size", "upload_signature", "bucket_id", "key", "version", "owner_id", "created_at", "user_metadata", "metadata") FROM stdin;
\.


--
-- Data for Name: s3_multipart_uploads_parts; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY "storage"."s3_multipart_uploads_parts" ("id", "upload_id", "size", "part_number", "bucket_id", "key", "etag", "owner_id", "version", "created_at") FROM stdin;
\.


--
-- Data for Name: vector_indexes; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY "storage"."vector_indexes" ("id", "name", "bucket_id", "data_type", "dimension", "distance_metric", "metadata_configuration", "created_at", "updated_at") FROM stdin;
\.


--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE SET; Schema: auth; Owner: supabase_auth_admin
--

SELECT pg_catalog.setval('"auth"."refresh_tokens_id_seq"', 11, true);


--
-- Name: agendamentos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."agendamentos_id_seq"', 4, true);


--
-- Name: aulas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."aulas_id_seq"', 1, false);


--
-- PostgreSQL database dump complete
--

-- \unrestrict yze87rSzXgt6w4CclDhXGXnm0e4AT3QnIedoiOSH2WbNcT7W1AzlBrOaKWOcVs4

RESET ALL;

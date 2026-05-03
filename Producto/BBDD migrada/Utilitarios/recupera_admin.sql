/* ============================================================
   UTILITARIO - Restaura usuario admin a valores de fábrica
   ============================================================ */

BEGIN;

UPDATE usuario
SET login            = 'admin@duoc.cl',
    hash_password    = 'c16fd958b85a1c94d872c219ea06ce8e80223239b1fcefb92ad978445ef095507244be44caae1d766e277b072c184cb3ffe4d0610716e989b2fe5a7c97bf3144',
    primer_apellido  = 'Administrador',
    segundo_apellido = NULL,
    nom              = 'del sistema',
    nom_preferido    = 'admin',
    cod_perfil       = 0,
    cod_carrera      = 0
WHERE id_usuario = 1;

COMMIT;

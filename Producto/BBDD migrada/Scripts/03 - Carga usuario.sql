/* ============================================================
   SCRIPT 03 - CARGA DE USUARIOS (DML)
   Contraseñas hasheadas con bcrypt.
   Contraseña inicial de cada usuario = su propio login.
   Ejemplo: admin@duoc.cl -> password: admin@duoc.cl
   ============================================================ */

BEGIN;

INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (1, 'admin@duoc.cl', '$2b$12$CTJ6GE3wnKWfwMJphUjqH.0KFybZhzNwe/rSC2ZZji.EfbeiOJfMK', 'Administrador', NULL, 'del sistema', 'admin', 0, 0);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (2, 'jmoya@duoc.cl', '$2b$12$RJTax7Fxq/o3NG4CKlss5.I0WvRzhguIuMbS0kJRQtnT2VtB5qROS', 'Moya', 'Plaza', 'Jéssica', 'Jéssica', 1, 1);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (3, 'maalvarez@duoc.cl', '$2b$12$jiyy8q67cp8o7PEq3.2NMeKr5/EibHS4ricyrLZ1S6ghs/fgjsAfq', 'Álvarez', 'Román', 'Marco', 'Marco', 2, 1);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (4, 'c.gonzalez6@profesor.duoc.cl', '$2b$12$vGKS..BJzWslWt54Wo6BX.TksHgmkV.2GnEsBqX3FXBHt1lLSZGrC', 'González', 'Figueroa', 'Cristian', 'Cristian', 2, 1);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (5, 'r.ceura@profesor.duoc.cl', '$2b$12$9hHd4yd6uUqAk3q2ZLRHkuu6ZYiwdwGC8lS6rJUfYvPgdEju7GzW6', 'Ceura', 'Vergara', 'Raúl', 'Raúl', 2, 1);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (6, 'hec.fonseca@profesor.duoc.cl', '$2b$12$8E6AK4Qn/KcL5xKb2lNJ2ObRVbij9Cy0O5Ft6WG3dHy4CbGTFiquO', 'Fonseca', 'Castillo', 'Héctor', 'Héctor', 2, 1);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (7, 'xi.castro@profesor.duoc.cl', '$2b$12$7844XWxLpNr1mx7jLy0Uu.IuAMpZL8pxHsV.IvpPWZXKAYKT.43V2', 'Castro', 'Arancibia', 'Ximena', 'Ximena', 2, 1);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (8, 'c.valenzuelair@profesor.duoc.cl', '$2b$12$EXWEtApJ7Wn8YsR79J7NEO2ACqrUEk5/x0BlV4qVE37oM0YPPfT5y', 'Valenzuela', 'Irrázabal', 'Carolina', 'Carolina', 2, 1);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (9, 'sa.navarret@profesor.duoc.cl', '$2b$12$Tii7cUe6Lhph0TUuhtADv.2M17Cejthxw9IRG0rM4tuGFyRqphMzW', 'Navarrete', 'Bustamante', 'Sandra', 'Sandra', 2, 1);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (10, 'fabi.arancibia@profesor.duoc.cl', '$2b$12$pD8fbXSlkCyOqrP77u63auscqEmWSGaZAjUI7B3fUBpOvTTlBtMKK', 'Arancibia', 'Severino', 'Fabián', 'Fabián', 2, 1);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (11, 'roci.guzman@profesor.duoc.cl', '$2b$12$/4buSgN.npqpkuZ1B7sH6.4Sc/wYLtPMmwNl6flJXfhTyPsuY4/b6', 'Guzmán', 'Acuña', 'Rocío', 'Rocío', 2, 1);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (12, 'al.camposa@profesor.duoc.cl', '$2b$12$/a2/eBeVe23uRtYD3JZEP.rkBJUadctlqdwq6iW52UcFbLxKWkUOy', 'Campos', 'Acuña', 'Alejandra', 'Alejandra', 2, 1);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (13, 'cr.madariagam@profesor.duoc.cl', '$2b$12$4c9E1jn7lTEqWOWcgJn/j.DNRHCIqvIFmq7OTAlzSKx8y7BmyyvfC', 'Madariaga', 'Martínez', 'Cristian', 'Cristian', 2, 1);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (14, 'i.inostroza@profesor.duoc.cl', '$2b$12$/OH7vNgeBgjHJz7t7qXpTedeXIZPzSglVhdf3dCaoplONXkmXp0Wq', 'Inostroza', 'Rodríguez', 'Isaac', 'Isaac', 2, 1);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (15, 'v.fuentealbav@profesor.duoc.cl', '$2b$12$77JmtQPzLWs/KmPPATueQu5gkE7bIea2LYTYXwBLGOygmhDuYwRyq', 'Fuentealba', 'Vargas', 'Víctor', 'Víctor', 2, 1);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (16, 'j.premolo@profesor.duoc.cl', '$2b$12$Nd9SO5JBfwqByRRryQviYuniTLMvgz7iZJyEp9k6nkVOU103bxolW', 'Prémolo', 'Yergues', 'Juan', 'Juan', 2, 1);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (17, 'car.perezz@profesor.duoc.cl', '$2b$12$4.5tZ4KRh6QCiX8IlZI6QuSfPzWd/X8HbuC6olYovrcStaLezK0c2', 'Pérez', 'Zúñiga', 'Carlos', 'Carlos', 2, 1);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (18, 'de.reglas@profesor.duoc.cl', '$2b$12$Zvdi0XDUupsqn7/nOs5Vyek8cehC6SIXH1MAW813I6J4EvrMcIS6G', 'Reglas', 'Villagra', 'Deyanira', 'Deyanira', 2, 1);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (19, 'dmunita@duoc.cl', '$2b$12$E2P.sTCYjVAUbuux89O1p.zT7Qm7.qstCTGAZlXb5zdyyW.5us1ke', 'Munita', 'Toro', 'Daniela', 'Daniela', 1, 2);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (20, 'pzamorano@duoc.cl', '$2b$12$Cxq3sDxShj.f3pyNUNlEeuxnByqwyr6fqI/hsohfFTFpHV4RfXX6a', 'Zamorano', 'Moreno', 'Paola', 'Paola', 2, 2);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (21, 'j.enero@profesor.duoc.cl', '$2b$12$eAaTUYK0LO/mqigFCyEaiecucECpPyro4Py6I2RPlqg4sKWozRbd.', 'Enero', 'Rivero', 'Juan Francisco', 'Juan', 2, 2);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (22, 'm.gutierrez2@profesor.duoc.cl', '$2b$12$RQPgODU5md3XNYRPFEYaoORLKZ0q77.Q2DC3nDNTzDd2EqHYmuqE6', 'Gutiérrez', 'Cortés', 'Mauricio', 'Mauricio', 2, 2);

-- Sincronizar secuencia SERIAL con el máximo ID insertado
SELECT setval(pg_get_serial_sequence('usuario', 'id_usuario'), 22);

COMMIT;

/* ============================================================
   SCRIPT 03 - CARGA DE USUARIOS (DML)
   Contraseñas hasheadas con bcrypt.
   Contraseña inicial de cada usuario = su propio login.
   ============================================================ */

BEGIN;

INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (1, 'admin@duoc.cl', '$2b$12$LqfqKdGuWyZtEokdyda/qeIE.xwwNB5tB/xJ7dQwQWLX3D3XLU5Ui', 'Administrador', NULL, 'del sistema', 'admin', 0, 0);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (2, 'jmoya@duoc.cl', '$2b$12$jrL5vymVU0/jU1lnFz7gMOZH0d3uFWbWtZmxnpO68wxfQUIlRuwZ2', 'Moya', 'Plaza', 'Jéssica', 'Jéssica', 1, 1);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (3, 'maalvarez@duoc.cl', '$2b$12$.9piGQQvX4AkcmyQDiw35uEz9lh8TsDnkOMvUlhMc2.yRNHc0rquG', 'Álvarez', 'Román', 'Marco', 'Marco', 2, 1);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (4, 'c.gonzalez6@profesor.duoc.cl', '$2b$12$IRO87y2Y1XmuZJLeWNLOgOsda9yAtcaemRS5qTxH7c/.mqGBNaNFS', 'González', 'Figueroa', 'Cristian', 'Cristian', 2, 1);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (5, 'r.ceura@profesor.duoc.cl', '$2b$12$UIAqfd/Ta2/PcEUxrgG0dewZaYvjkv5gJadLko9fksKesDq9xHFLS', 'Ceura', 'Vergara', 'Raúl', 'Raúl', 2, 1);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (6, 'hec.fonseca@profesor.duoc.cl', '$2b$12$N4GG/PtYbN/vR16C9IWfC.3KdfgxiDn26DxfoRyODitP41tjn.zim', 'Fonseca', 'Castillo', 'Héctor', 'Héctor', 2, 1);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (7, 'xi.castro@profesor.duoc.cl', '$2b$12$BiZwBXge7fEMSr5qKLBXzeNxqo9t2OaKFmKxOUzlrVuPceDnB5J4W', 'Castro', 'Arancibia', 'Ximena', 'Ximena', 2, 1);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (8, 'c.valenzuelair@profesor.duoc.cl', '$2b$12$ooqagFP8g9PHLLw2/7cFmOhGMOW7FWn3Z0Ot50wlxiQwFwdZUnqqG', 'Valenzuela', 'Irrázabal', 'Carolina', 'Carolina', 2, 1);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (9, 'sa.navarret@profesor.duoc.cl', '$2b$12$szu2SEuEIDwOz/rPBwT1HObHpzVLR0zGwQ3PnQmkPRqlpkw7dLGv.', 'Navarrete', 'Bustamante', 'Sandra', 'Sandra', 2, 1);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (10, 'fabi.arancibia@profesor.duoc.cl', '$2b$12$3Uxdhanpdkz9wcjClly52uYI2V6AI9LNYTlsB0N5n.Yv0RUy1LFLq', 'Arancibia', 'Severino', 'Fabián', 'Fabián', 2, 1);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (11, 'roci.guzman@profesor.duoc.cl', '$2b$12$29hTd3HKIQOSNFtQMrFOmOIa.7XtrCJNbJVkcM2YJJSw6LsHgNZ7e', 'Guzmán', 'Acuña', 'Rocío', 'Rocío', 2, 1);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (12, 'al.camposa@profesor.duoc.cl', '$2b$12$i1TPJ5ElmqAl39E.vzHQNunz7iNHd5xqgIHMfc99malkw1OlSH6oW', 'Campos', 'Acuña', 'Alejandra', 'Alejandra', 2, 1);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (13, 'cr.madariagam@profesor.duoc.cl', '$2b$12$z/uGSWSm.joy0yV7vBSdkehnKibcosIjanmGSoVasBlR4jXqt.hfW', 'Madariaga', 'Martínez', 'Cristian', 'Cristian', 2, 1);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (14, 'i.inostroza@profesor.duoc.cl', '$2b$12$uIb2NrlnO08ugzvkJ3sH5Od4C.x98OCfdfcsMmU9/xUaWk1kJHUJ2', 'Inostroza', 'Rodríguez', 'Isaac', 'Isaac', 2, 1);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (15, 'v.fuentealbav@profesor.duoc.cl', '$2b$12$83dmW/.s/imMCSJCok6ufuFKKRLSCt6h2GM9lK/O79YItO3kbM7ta', 'Fuentealba', 'Vargas', 'Víctor', 'Víctor', 2, 1);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (16, 'j.premolo@profesor.duoc.cl', '$2b$12$nv6mPCYFZvslJ6H3S.9Jh.0Pa2gbosO6s/RpmX7.TN9f5sVKwDIai', 'Prémolo', 'Yergues', 'Juan', 'Juan', 2, 1);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (17, 'car.perezz@profesor.duoc.cl', '$2b$12$7vXeDImN5rqepRtzx8x1qec3qtmD4cpHV20zBRa40/jgdQ7LZNf0a', 'Pérez', 'Zúñiga', 'Carlos', 'Carlos', 2, 1);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (18, 'de.reglas@profesor.duoc.cl', '$2b$12$LPZmUW9LEPfbeQEaAnnO0uX9Fm1Qnr//tXV.sQR8ud/OP/upjWX9a', 'Reglas', 'Villagra', 'Deyanira', 'Deyanira', 2, 1);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (19, 'dmunita@duoc.cl', '$2b$12$JTmUoQIi.SUU3Pjnd6uSV.W73w1PqIs1FQGpxDLloIfqFJBTsVxNe', 'Munita', 'Toro', 'Daniela', 'Daniela', 1, 2);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (20, 'pzamorano@duoc.cl', '$2b$12$otuWaWmkQd2GrnnFj9yE9uz1pBDZLl/QSPkklKmHg82wz4L3jm5zK', 'Zamorano', 'Moreno', 'Paola', 'Paola', 2, 2);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (21, 'j.enero@profesor.duoc.cl', '$2b$12$gXa/yNM4XHSa/80f7ac.nuJc73yR/sKN1G/6ed1Y6RXQeB2LmsljC', 'Enero', 'Rivero', 'Juan Francisco', 'Juan', 2, 2);
INSERT INTO usuario (id_usuario, login, hash_password, primer_apellido, segundo_apellido, nom, nom_preferido, cod_perfil, cod_carrera) VALUES (22, 'm.gutierrez2@profesor.duoc.cl', '$2b$12$dkUpubXHe9qcMVw82yLDquuI8ZcfY2K.Vq9Ik1wsme8ASSixXZYTW', 'Gutiérrez', 'Cortés', 'Mauricio', 'Mauricio', 2, 2);

-- Sincronizar secuencia SERIAL con el máximo ID insertado
SELECT setval(pg_get_serial_sequence('usuario', 'id_usuario'), 22);

COMMIT;

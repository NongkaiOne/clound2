-- -----------------------------------------------------
-- Sample Data
-- -----------------------------------------------------

USE `mallmap`;
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE `User`;
TRUNCATE TABLE `Role`;
TRUNCATE TABLE `StoreCategory`;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO `Role` (RoleName) VALUES
('Admin'),
('StoreOwner'),
('Customer');

-- Password for all users is: 123456
INSERT INTO mallmap.User
(UserName, Email, PasswordHash, RoleID, CreatedAt, UpdatedAt)
VALUES
('admin1', 'admin1@mail.com', '$2b$12$KIXbVfP1z/9rGZ.b.L7MueqU0uV.gK0h5O7fIu.Wv7h0.G.C7.z8.', 1, NOW(), NOW()),
('storeOwner1', 'owner1@mail.com', '$2b$12$KIXbVfP1z/9rGZ.b.L7MueqU0uV.gK0h5O7fIu.Wv7h0.G.C7.z8.', 2, NOW(), NOW()),
('customer1', 'customer1@mail.com', '$2b$12$KIXbVfP1z/9rGZ.b.L7MueqU0uV.gK0h5O7fIu.Wv7h0.G.C7.z8.', 3, NOW(), NOW());


INSERT INTO mallmap.StoreCategory (StoreCategoryName) VALUES
('Food'),
('Fashion'),
('Electronics');

INSERT INTO mallmap.mall (MallName, Location)
VALUES ('Central Mall', 'Bangkok');

INSERT INTO mallmap.floor (FloorName, MallID, MapImageURL)
VALUES ('Floor 1', 1, 'map1.png');

INSERT INTO mallmap.Store
(UserID, StoreName, StoreCategoryID, Phone, LogoURL, FloorID, PosX, PosY)
VALUES
(2, 'Yamazaki', 1, '0912345678', 'http://example.com/logoA.png', 1, 10.5, 20.5),
(2, 'ElectroWorld', 3, '0987654321', 'http://example.com/logoB.png', 1, 15.0, 25.0);
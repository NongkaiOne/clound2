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
(StoreID, FloorID, MallID,StoreName,Description,StoreCategoryName,StoreCategoryIcon,FloorName,FloorID, PosX, PosY, StoreCategoryID, UserID, LogoURL)
VALUES
(1, 1, 1, 'Store 1', 'Description 1', 'Food', 'food-icon.png', 'Floor 1', '1', 100.0, 200.0, 1, 2, 'logo1.png'),
(2, 1, 1, 'Store 2', 'Description 2', 'Fashion', 'fashion-icon.png', 'Floor 1', '1', 150.0, 250.0, 2, 2, 'logo2.png'),
(3, 1, 1, 'Store 3', 'Description 3', 'Electronics', 'electronics-icon.png', 'Floor 1', '1', 200.0, 300.0, 3, 2, 'logo3.png');
CREATE TABLE IF NOT EXISTS posts (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    content VARCHAR(255) NOT NULL,
    published BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);


INSERT INTO posts (title, content)
VALUES
('The Morning Boost', 'Start your day with a banana, oats, and almond milk smoothie.'),
('Green Power', 'Blend spinach, kale, apple, and lemon juice for a healthy green drink.'),
('Tropical Bliss', 'A mix of pineapple, mango, and coconut water for a taste of paradise.'),
('Berry Fusion', 'Combine strawberries, blueberries, and yogurt for a creamy delight.'),
('Protein Punch', 'Add protein powder, peanut butter, and banana for post-workout energy.'),
('Carrot Glow', 'Blend carrots, oranges, and ginger for radiant skin.'),
('Chocolate Dream', 'Mix cocoa, milk, and dates for a guilt-free dessert smoothie.'),
('Citrus Refresh', 'Lemon, orange, and mint combined for a refreshing detox drink.'),
('Apple Spice', 'Apples, cinnamon, and oats make a cozy, comforting smoothie.'),
('Minty Melon', 'Watermelon, mint, and lime juice for a cool summer treat.');


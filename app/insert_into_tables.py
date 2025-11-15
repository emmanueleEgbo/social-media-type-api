# from app.models import Post, User
# from app.session_settup import session

# # Create 20 posts for 10 users
# posts_data = [
#     {"title": "Morning Energy Boost", "content": "Blend banana, oats, and almond milk for a quick energy drink."},
#     {"title": "Green Detox", "content": "Mix spinach, cucumber, apple, and lemon juice for cleansing."},
#     {"title": "Berry Delight", "content": "Combine blueberries, strawberries, and Greek yogurt for antioxidants."},
#     {"title": "Tropical Breeze", "content": "Blend pineapple, mango, and coconut water for hydration."},
#     {"title": "Protein Punch", "content": "Add peanut butter, banana, and protein powder to oat milk."},
#     {"title": "Avocado Dream", "content": "Creamy avocado with kale and honey for healthy fats."},
#     {"title": "Citrus Glow", "content": "Blend orange, lemon, and carrots to boost immunity."},
#     {"title": "Classic Strawberry", "content": "Strawberries, banana, and yogurt — a timeless smoothie."},
#     {"title": "Choco Energy", "content": "Cocoa powder, oats, and almond milk for a guilt-free treat."},
#     {"title": "Minty Fresh", "content": "Cucumber, mint, and lime for a cool afternoon refreshment."},
#     {"title": "Golden Recovery", "content": "Turmeric, ginger, and coconut milk for post-workout healing."},
#     {"title": "Apple Power", "content": "Apple, cinnamon, and oat milk — comforting and healthy."},
#     {"title": "Berry Sunrise", "content": "Blueberries and orange juice to start your day right."},
#     {"title": "Tropical Fuel", "content": "Mango, banana, and coconut milk for a full-bodied taste."},
#     {"title": "Peach Cooler", "content": "Peach, yogurt, and honey for a sweet summer vibe."},
#     {"title": "Cocoa Rush", "content": "Banana, cocoa, and peanut butter for a filling blend."},
#     {"title": "Fresh Greens", "content": "Spinach, kale, celery, and green apple for detox power."},
#     {"title": "Sunset Smoothie", "content": "Papaya, orange, and carrot — the evening blend."},
#     {"title": "Oat Morning", "content": "Oats, almond butter, and soy milk to kickstart the day."},
#     {"title": "Berry Blast", "content": "Mixed berries and chia seeds for a fiber-rich snack."},
# ]

# # Assign posts to users in round-robin fashion
# user_ids = [u.id for u in session.query(User).all()]

# for idx, data in enumerate(posts_data):
#     owner_id = user_ids[idx % len(user_ids)]
#     post = Post(
#         title=data["title"],
#         content=data["content"],
#         owner_id=owner_id
#     )
#     session.add(post)

# session.commit()
# print("20 posts successfully added!")
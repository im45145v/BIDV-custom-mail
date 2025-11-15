#!/usr/bin/env python3
"""
Verification script to test the AI BI pipeline end-to-end.
"""
import sys
from pathlib import Path

print("=" * 60)
print("AI BI Streamlit Reports - Verification Script")
print("=" * 60)
print()

# Test 1: Data Generation
print("Test 1: Data Generation")
print("-" * 60)
try:
    from data import generator
    customers_df, orders_df = generator.generate_synthetic_data()
    generator.save_data(customers_df, orders_df)
    print(f"✓ Generated {len(customers_df)} customers")
    print(f"✓ Generated {len(orders_df)} orders")
    print(f"✓ Data saved to CSV files")
    test1_passed = True
except Exception as e:
    print(f"✗ Error: {e}")
    test1_passed = False
print()

# Test 2: BI Analysis
print("Test 2: BI Analysis & KPIs")
print("-" * 60)
try:
    from bi import analysis
    customers_df, orders_df = generator.load_data()
    customer_id = customers_df.iloc[0]['customer_id']
    customer_name = customers_df.iloc[0]['name']
    
    kpis = analysis.calculate_customer_kpis(customer_id, customers_df, orders_df)
    print(f"✓ Calculated KPIs for {customer_name} ({customer_id})")
    print(f"  - Total Spend: ₹{kpis['total_spend']:,.2f}")
    print(f"  - Orders: {kpis['orders_count']}")
    print(f"  - AOV: ₹{kpis['average_order_value']:,.2f}")
    print(f"  - Frequency: {kpis['order_frequency']:.2f} orders/month")
    print(f"  - Top Category: {kpis['top_category']}")
    test2_passed = True
except Exception as e:
    print(f"✗ Error: {e}")
    test2_passed = False
print()

# Test 3: Visualization
print("Test 3: Chart Generation")
print("-" * 60)
try:
    from bi import visuals
    import config
    
    trend_df = analysis.get_recent_trend(customer_id, orders_df, days=90)
    category_df = analysis.get_category_distribution(customer_id, orders_df)
    
    subdirs = config.get_customer_subdirs(customer_id)
    charts = visuals.save_all_customer_charts(
        customer_id,
        customer_name,
        trend_df,
        category_df,
        subdirs['charts']
    )
    
    print(f"✓ Generated charts for {customer_name}")
    for chart_name, chart_path in charts.items():
        print(f"  - {chart_name}: {chart_path.name}")
    test3_passed = True
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    test3_passed = False
print()

# Test 4: AI Image Generation (Placeholder)
print("Test 4: Image Generation")
print("-" * 60)
try:
    from media import ai_images
    
    customer = customers_df[customers_df['customer_id'] == customer_id].iloc[0]
    cover_path = ai_images.generate_customer_image(
        customer['segment'],
        customer['interests'],
        subdirs['images'] / "ai_cover.png",
        use_openai=False,
        use_gemini=False
    )
    
    if cover_path and cover_path.exists():
        print(f"✓ Generated placeholder image for {customer_name}")
        print(f"  - Segment: {customer['segment']}")
        print(f"  - Interests: {', '.join(customer['interests'][:3])}")
        print(f"  - Path: {cover_path}")
        test4_passed = True
    else:
        print(f"✗ Failed to generate image")
        test4_passed = False
except Exception as e:
    print(f"✗ Error: {e}")
    test4_passed = False
print()

# Test 5: Email Formatting
print("Test 5: Email Template")
print("-" * 60)
try:
    from notifier import email_webhook
    
    html = email_webhook.format_customer_email(
        customer_name=customer_name,
        customer_email=customer['email'],
        segment=customer['segment'],
        kpis=kpis,
        video_url=None,
        charts_urls=None
    )
    
    print(f"✓ Generated HTML email template")
    print(f"  - Length: {len(html)} characters")
    print(f"  - Contains customer name: {'✓' if customer_name in html else '✗'}")
    print(f"  - Contains KPIs: {'✓' if str(kpis['total_spend']) in html else '✗'}")
    test5_passed = True
except Exception as e:
    print(f"✗ Error: {e}")
    test5_passed = False
print()

# Summary
print("=" * 60)
print("Test Summary")
print("=" * 60)
tests = [
    ("Data Generation", test1_passed),
    ("BI Analysis", test2_passed),
    ("Chart Generation", test3_passed),
    ("Image Generation", test4_passed),
    ("Email Template", test5_passed),
]

passed = sum(1 for _, result in tests if result)
total = len(tests)

for test_name, result in tests:
    status = "✓ PASS" if result else "✗ FAIL"
    print(f"{test_name:.<40} {status}")

print()
print(f"Results: {passed}/{total} tests passed")
print()

if passed == total:
    print("🎉 All core functionality verified!")
    print()
    print("Next steps:")
    print("  1. Run: streamlit run app.py")
    print("  2. Open browser to http://localhost:8501")
    print("  3. Click 'Generate Data' (if not done)")
    print("  4. Select a customer")
    print("  5. Explore KPIs and charts")
    print("  6. Generate audio, video, and send email")
    sys.exit(0)
else:
    print("⚠️  Some tests failed. Please review errors above.")
    sys.exit(1)

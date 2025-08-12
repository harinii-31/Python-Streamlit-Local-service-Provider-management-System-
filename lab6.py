import streamlit as st
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(
    page_title="Local Service Provider Management System",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .booking-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .sidebar-header {
        color: #1f77b4;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'bookings' not in st.session_state:
    st.session_state.bookings = []
if 'destinations' not in st.session_state:
    # Sample service provider data
    st.session_state.destinations = [
        {"name": "ABC Plumbing Services", "country": "Local Area", "price": 120, "rating": 4.8, "category": "Plumbing"},
        {"name": "QuickFix Electrical", "country": "Downtown", "price": 150, "rating": 4.9, "category": "Electrical"},
        {"name": "GreenThumb Landscaping", "country": "Suburbs", "price": 200, "rating": 4.7, "category": "Landscaping"},
        {"name": "CleanSweep Cleaning Co.", "country": "City Center", "price": 80, "rating": 4.6, "category": "Cleaning"},
        {"name": "HomeShine Maintenance", "country": "North Side", "price": 90, "rating": 4.8, "category": "Maintenance"},
        {"name": "ProCarpet Care", "country": "West End", "price": 180, "rating": 4.9, "category": "Carpet Cleaning"},
        {"name": "Elite HVAC Solutions", "country": "East District", "price": 110, "rating": 4.5, "category": "HVAC"},
        {"name": "Handyman Heroes", "country": "South Zone", "price": 160, "rating": 4.7, "category": "General Repair"}
    ]

# Sidebar Navigation
st.sidebar.markdown('<p class="sidebar-header">🧭 Navigation</p>', unsafe_allow_html=True)
page = st.sidebar.selectbox("Select Page", ["Dashboard", "Book Service", "My Bookings", "Service Providers", "Analytics"])

# Main header
st.markdown('<h1 class="main-header">🔧 Local Service Provider Management System</h1>', unsafe_allow_html=True)

# Dashboard Page
if page == "Dashboard":
    st.subheader("📊 Dashboard Overview")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Bookings", len(st.session_state.bookings), delta="+2")
    
    with col2:
        total_revenue = sum([booking['price'] for booking in st.session_state.bookings])
        st.metric("Total Revenue", f"${total_revenue:,}", delta="+15%")
    
    with col3:
        st.metric("Available Service Providers", len(st.session_state.destinations))
    
    with col4:
        avg_rating = sum([dest['rating'] for dest in st.session_state.destinations]) / len(st.session_state.destinations)
        st.metric("Avg Provider Rating", f"{avg_rating:.1f}⭐")
    
    st.divider()
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔧 Popular Service Providers")
        if st.session_state.bookings:
            booking_df = pd.DataFrame(st.session_state.bookings)
            dest_counts = booking_df['destination'].value_counts()
            fig = px.pie(values=dest_counts.values, names=dest_counts.index,
                        title="Booking Distribution by Service Provider")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No bookings yet. Book your first service!")
    
    with col2:
        st.subheader("💰 Price Range Analysis")
        dest_df = pd.DataFrame(st.session_state.destinations)
        fig = px.histogram(dest_df, x='price', nbins=10, title="Service Provider Price Distribution",
                          labels={'price': 'Price ($)', 'count': 'Number of Providers'})
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

# Book Service Page
elif page == "Book Service":
    st.subheader("🎫 Book Your Service Appointment")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Service Details")
        
        # Booking form
        with st.form("booking_form"):
            traveler_name = st.text_input("Customer Name", placeholder="Enter your full name")
            
            destination_names = [dest['name'] for dest in st.session_state.destinations]
            selected_dest = st.selectbox("Choose Service Provider", destination_names)
            
            # Get selected destination details
            dest_details = next(dest for dest in st.session_state.destinations if dest['name'] == selected_dest)
            
            col_a, col_b = st.columns(2)
            with col_a:
                departure_date = st.date_input("Service Date", min_value=datetime.now().date())
            with col_b:
                duration = st.selectbox("Service Duration (hours)", [1, 2, 3, 4, 6, 8], index=2)
            
            travelers = st.number_input("Number of Service Units", min_value=1, max_value=10, value=1)
            
            travel_class = st.selectbox("Service Priority", ["Standard", "Priority", "Emergency"])
            
            # Calculate total price
            base_price = dest_details['price']
            class_multiplier = {"Standard": 1.0, "Priority": 1.5, "Emergency": 2.0}
            total_price = base_price * travelers * class_multiplier[travel_class] * (duration / 3)
            
            st.info(f"💰 Total Price: ${total_price:,.2f}")
            
            submitted = st.form_submit_button("Book Now", type="primary")
            
            if submitted:
                if traveler_name:
                    booking = {
                        'id': len(st.session_state.bookings) + 1,
                        'traveler': traveler_name,
                        'destination': selected_dest,
                        'departure': departure_date.strftime('%Y-%m-%d'),
                        'duration': duration,
                        'travelers': travelers,
                        'class': travel_class,
                        'price': total_price,
                        'status': 'Confirmed',
                        'booking_date': datetime.now().strftime('%Y-%m-%d %H:%M')
                    }
                    st.session_state.bookings.append(booking)
                    st.success(f"🎉 Service booking confirmed! Booking ID: {booking['id']}")
                    st.balloons()
                else:
                    st.error("Please enter customer name")
    
    with col2:
        st.markdown("### Service Provider Preview")
        if selected_dest:
            dest_info = dest_details
            
            # Destination card
            st.markdown(f"""
            <div class="booking-card">
                <h3>🔧 {dest_info['name']}</h3>
                <p><strong>Service Area:</strong> {dest_info['country']}</p>
                <p><strong>Category:</strong> {dest_info['category']}</p>
                <p><strong>Rating:</strong> {dest_info['rating']}⭐</p>
                <p><strong>Base Rate (per hour):</strong> ${dest_info['price']:,}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Price breakdown
            if 'total_price' in locals():
                st.markdown("### 💳 Price Breakdown")
                st.write(f"Base rate per hour: ${base_price:,}")
                st.write(f"Service duration: {duration} hours")
                st.write(f"Number of service units: {travelers}")
                st.write(f"Priority multiplier ({travel_class}): {class_multiplier[travel_class]}x")
                st.write(f"*Total: ${total_price:,.2f}*")

# My Bookings Page
elif page == "My Bookings":
    st.subheader("📋 My Service Bookings")
    
    if st.session_state.bookings:
        # Filter options
        col1, col2 = st.columns([1, 1])
        with col1:
            status_filter = st.selectbox("Filter by Status", ["All", "Confirmed", "Cancelled", "Completed"])
        
        # Display bookings
        for booking in st.session_state.bookings:
            if status_filter == "All" or booking['status'] == status_filter:
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"""
                    <div class="booking-card">
                        <h4>🎫 Booking #{booking['id']} - {booking['destination']}</h4>
                        <p><strong>Customer:</strong> {booking['traveler']}</p>
                        <p><strong>Service Date:</strong> {booking['departure']} | <strong>Duration:</strong> {booking['duration']} hours</p>
                        <p><strong>Service Units:</strong> {booking['travelers']} | <strong>Priority:</strong> {booking['class']}</p>
                        <p><strong>Total Price:</strong> ${booking['price']:,.2f}</p>
                        <p><strong>Status:</strong> <span style="color: green;">{booking['status']}</span></p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if st.button("✏ Modify", key=f"modify_{booking['id']}"):
                        st.info("Modification feature coming soon!")
                
                with col3:
                    if st.button("❌ Cancel", key=f"cancel_{booking['id']}"):
                        booking['status'] = 'Cancelled'
                        st.rerun()
    else:
        st.info("No bookings found. Book your first service!")

# Service Providers Page
elif page == "Service Providers":
    st.subheader("🌍 Explore Service Providers")
    
    # Filter controls
    col1, col2, col3 = st.columns(3)
    with col1:
        category_filter = st.selectbox("Category", ["All"] + list(set([dest['category'] for dest in st.session_state.destinations])))
    with col2:
        price_range = st.slider("Price Range ($/hour)", 0, 250, (0, 250))
    with col3:
        min_rating = st.slider("Minimum Rating", 0.0, 5.0, 0.0, 0.1)
    
    # Filter destinations
    filtered_destinations = []
    for dest in st.session_state.destinations:
        if (category_filter == "All" or dest['category'] == category_filter) and \
           (price_range[0] <= dest['price'] <= price_range[1]) and \
           (dest['rating'] >= min_rating):
            filtered_destinations.append(dest)
    
    # Display destinations in cards
    cols = st.columns(3)
    for i, dest in enumerate(filtered_destinations):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="booking-card">
                <h4>🔧 {dest['name']}</h4>
                <p><strong>Service Area:</strong> {dest['country']}</p>
                <p><strong>Category:</strong> {dest['category']}</p>
                <p><strong>Rating:</strong> {dest['rating']}⭐</p>
                <p><strong>Rate:</strong> ${dest['price']:,}/hour</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Select Provider", key=f"select_{dest['name']}"):
                st.session_state.selected_destination = dest['name']
                st.switch_page("Book Service")

# Analytics Page
elif page == "Analytics":
    st.subheader("📈 Service Analytics")
    
    # Generate sample analytics data
    if st.session_state.bookings:
        booking_df = pd.DataFrame(st.session_state.bookings)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Revenue by Service Provider")
            revenue_by_dest = booking_df.groupby('destination')['price'].sum().reset_index()
            fig = px.bar(revenue_by_dest, x='destination', y='price',
                        title="Revenue by Service Provider",
                        labels={'price': 'Revenue ($)', 'destination': 'Service Provider'})
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🏷 Bookings by Service Priority")
            class_counts = booking_df['class'].value_counts()
            fig = px.pie(values=class_counts.values, names=class_counts.index,
                        title="Service Priority Distribution")
            st.plotly_chart(fig, use_container_width=True)
        
        # Time series analysis
        st.markdown("### 📅 Booking Trends")
        booking_df['booking_date'] = pd.to_datetime(booking_df['booking_date'])
        daily_bookings = booking_df.groupby(booking_df['booking_date'].dt.date).size().reset_index()
        daily_bookings.columns = ['date', 'bookings']
        
        fig = px.line(daily_bookings, x='date', y='bookings',
                     title="Daily Booking Trends",
                     labels={'bookings': 'Number of Bookings', 'date': 'Date'})
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.info("No booking data available for analytics. Make some bookings first!")
    
    # Service provider analytics
    st.markdown("### 🔧 Service Provider Analytics")
    dest_df = pd.DataFrame(st.session_state.destinations)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.scatter(dest_df, x='price', y='rating', color='category',
                        size='price', hover_name='name',
                        title="Rate vs Rating by Category")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        category_stats = dest_df.groupby('category').agg({
            'price': 'mean',
            'rating': 'mean'
        }).reset_index()
        
        fig = px.bar(category_stats, x='category', y='price',
                    title="Average Rate by Category",
                    labels={'price': 'Average Rate ($/hour)', 'category': 'Category'})
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Local Service Provider Management System - Built with Streamlit")
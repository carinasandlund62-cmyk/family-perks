
import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path
import hashlib
import html

# ==========================================
# FAMILY PERKS 3.0
# ==========================================

st.set_page_config(
    page_title="Family Perks",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

GREEN = "#326B49"
DARK = "#234B34"
SAGE = "#DFEDDF"
MINT = "#83B692"
WHITE = "#FFFFFF"

PALETTE = [
    "#326B49",
    "#60966A",
    "#83B692",
    "#B5CDAA",
    "#D7E5D3",
    "#DDBB83"
]

# ==========================================
# APP DESIGN
# ==========================================

st.markdown("""
<style>

.stApp {
    background: #DFEDDF;
    color: #234B34;
}

[data-testid="stHeader"] {
    background: #DFEDDF;
}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4,
.stApp h5,
.stApp h6 {
    color: #234B34 !important;
    font-weight: 750;
    letter-spacing: -0.5px;
}

.stApp p,
.stApp label {
    color: #234B34;
}

[data-testid="stCaptionContainer"] p {
    color: #536D5B !important;
}

[data-testid="stMetric"] {
    background: white;
    padding: 18px;
    border-radius: 18px;
    border: 1px solid #D3E3D4;
}

[data-testid="stMetricValue"] {
    color: #234B34 !important;
    font-weight: 750;
}

[data-testid="stMetricLabel"] {
    color: #536D5B !important;
}

.stButton > button,
.stFormSubmitButton > button {
    background: #326B49;
    color: white !important;
    border: none;
    border-radius: 12px;
    min-height: 45px;
    font-weight: 650;
}

.stButton > button p,
.stFormSubmitButton > button p {
    color: white !important;
}

.stButton > button:hover {
    background: #234B34;
    color: white !important;
}

.stButton > button:disabled {
    background: #D5E2D4;
    color: #536D5B !important;
}

.stButton > button:disabled p {
    color: #536D5B !important;
}

.stProgress > div > div {
    background: #C2D5C3;
}

.stProgress > div > div > div > div {
    background: #43885C;
}

[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    color: #234B34 !important;
    border-radius: 12px;
}

[data-baseweb="input"] {
    background: #FFFFFF !important;
}

.hero {
    background: #234B34;
    border-radius: 24px;
    padding: 26px;
    margin-bottom: 18px;
}

.hero h1,
.hero h2,
.hero h3,
.hero p,
.hero span {
    color: #FFFFFF !important;
}

.hero .eyebrow {
    color: #BCE1C0 !important;
    font-size: 12px;
    letter-spacing: 2px;
    font-weight: 700;
}

.card {
    background: #FFFFFF;
    border: 1px solid #D3E3D4;
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 12px;
}

.card p {
    margin-bottom: 5px;
}

.receipt {
    background: #FFFFFF;
    padding: 25px;
    border-radius: 18px;
    border: 1px solid #D3E3D4;
    margin: 12px 0;
}

.receipt-row {
    display: flex;
    justify-content: space-between;
    gap: 15px;
    padding: 10px 0;
    border-bottom: 1px dashed #DFE8DF;
    color: #234B34;
    font-size: 14px;
}

.receipt-total {
    font-size: 22px;
    font-weight: 750;
    color: #234B34;
    display: flex;
    justify-content: space-between;
    padding-top: 20px;
}

.product-row {
    background: white;
    border-radius: 14px;
    padding: 14px;
    margin-bottom: 8px;
    border: 1px solid #D3E3D4;
}

.product-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 15px;
}

.product-name {
    color: #234B34;
    font-weight: 650;
    font-size: 14px;
}

.product-count {
    color: #536D5B;
    font-size: 12px;
    white-space: nowrap;
}

.track {
    background: #E4EEE3;
    height: 10px;
    border-radius: 10px;
    overflow: hidden;
    margin-top: 10px;
}

.fill {
    background: #60966A;
    height: 100%;
    border-radius: 10px;
}

.reward {
    background: #FFFFFF;
    border-radius: 22px;
    padding: 22px;
    border: 1px solid #D3E3D4;
}

.reward-number {
    color: #326B49;
    font-size: 36px;
    font-weight: 800;
}

.offer-badge {
    background: #DDEFE0;
    color: #234B34;
    padding: 7px 12px;
    border-radius: 10px;
    display: inline-block;
    font-size: 20px;
    font-weight: 750;
}

.wallet {
    background: linear-gradient(
        135deg, #193E2A, #43845C
    );
    color: white;
    border-radius: 25px;
    padding: 28px;
    max-width: 420px;
    margin: 15px auto;
    box-shadow: 0 12px 25px #234B3430;
}

.wallet h1,
.wallet h2,
.wallet h3,
.wallet p {
    color: white !important;
}

.wallet-code {
    background: white;
    color: #193E2A;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
}

[data-testid="stVegaLiteChart"] {
    background: white;
    padding: 12px;
    border-radius: 18px;
    border: 1px solid #D3E3D4;
}

@media (max-width: 600px) {
    .block-container {
        padding-left: 15px;
        padding-right: 15px;
        padding-top: 1rem;
    }

    .hero {
        padding: 20px;
    }

    .stApp h1 {
        font-size: 30px !important;
    }
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# DATABASE
# ==========================================

@st.cache_data
def load_data():

    path = Path(__file__).parent / "receipt_database.xlsx"

    data = pd.read_excel(
        path,
        sheet_name="Synthetic Receipts"
    )

    data["Date"] = pd.to_datetime(
        data["Date"], errors="coerce"
    )

    data["Consumer ID"] = (
        data["Consumer ID"].astype(str)
    )

    data["Receipt ID"] = (
        data["Receipt ID"].astype(str)
    )

    data["Product Name"] = (
        data["Product Name"]
        .fillna("Unknown product")
        .astype(str)
        .str.strip()
    )

    for col in [
        "Line Total",
        "Total Spend",
        "Quantity"
    ]:
        data[col] = pd.to_numeric(
            data[col],
            errors="coerce"
        ).fillna(0)

    return data


try:
    df = load_data()

except Exception as error:

    st.error(
        "The receipt database could not be loaded. "
        "Check that receipt_database.xlsx is in "
        "the same folder as app.py."
    )

    st.caption(str(error))
    st.stop()


def money(value):
    return f"£{float(value):,.2f}"


# ==========================================
# PRODUCT CATEGORIES
# ==========================================

def category(product):

    p = product.lower()

    if any(x in p for x in [
        "pampers", "nappies", "baby",
        "diapers"
    ]):
        return "Baby care"

    if any(x in p for x in [
        "fairy", "ariel", "lenor",
        "laundry", "detergent", "bleach",
        "cleaner", "washing", "dishwasher"
    ]):
        return "Cleaning"

    if any(x in p for x in [
        "shampoo", "pantene", "toothpaste",
        "oral-b", "oral b", "deodorant",
        "conditioner", "head and shoulders",
        "head & shoulders", "razor",
        "gillette", "body wash"
    ]):
        return "Personal care"

    if any(x in p for x in [
        "bread", "milk", "fruit", "apple",
        "banana", "chicken", "beef", "rice",
        "pasta", "cheese", "yoghurt", "egg",
        "potato", "tomato", "cereal",
        "juice", "fish", "vegetable",
        "grape", "pepper", "hovis",
        "warburtons", "kingsmill", "alpro",
        "peelers", "butter", "biscuit",
        "chocolate", "orange", "salad",
        "coffee", "tea", "crisps"
    ]):
        return "Groceries"

    return "Other / unclassified"


df["Category"] = df["Product Name"].apply(category)

ICONS = {
    "Groceries": "🛒",
    "Cleaning": "🫧",
    "Personal care": "🧴",
    "Baby care": "🍼",
    "Other / unclassified": "📦"
}

OFFER_VALUES = {
    "fairy": 0.50,
    "ariel": 1.00,
    "lenor": 0.75,
    "pantene": 0.75,
    "oral-b": 0.50,
    "oral b": 0.50,
    "head and shoulders": 0.75,
    "head & shoulders": 0.75,
    "pampers": 2.00,
    "gillette": 1.00
}


# ==========================================
# BEAUTIFUL CHARTS
# ==========================================

def chart_style(chart):

    return (
        chart
        .configure_view(stroke=None)
        .configure(background="#FFFFFF")
        .configure_axis(
            labelColor=DARK,
            titleColor=DARK,
            labelFontSize=12,
            titleFontSize=12,
            gridColor="#E8F0E8",
            domain=False,
            ticks=False
        )
        .configure_legend(
            labelColor=DARK,
            titleColor=DARK,
            labelFontSize=12
        )
    )


def horizontal_chart(
    series,
    label="Product",
    value="Value",
    currency=False,
    percentage=False
):

    series = series.dropna()

    if series.empty:
        st.info("Not enough data for this chart yet.")
        return

    data = series.rename("Amount").reset_index()

    data.columns = ["Name", "Amount"]

    if currency:
        data["Display"] = data["Amount"].map(money)
    elif percentage:
        data["Display"] = data["Amount"].map(
            lambda x: f"{x:.1f}%"
        )
    else:
        data["Display"] = data["Amount"].map(
            lambda x: f"{x:,.0f}"
        )

    data = data.sort_values(
        "Amount",
        ascending=False
    )

    maximum = float(data["Amount"].max())

    if percentage:
        upper = 120
    else:
        upper = max(1, maximum * 1.28)

    base = alt.Chart(data).encode(
        y=alt.Y(
            "Name:N",
            sort="-x",
            title=None,
            axis=alt.Axis(
                labelLimit=380,
                labelPadding=12
            )
        ),
        x=alt.X(
            "Amount:Q",
            title=value,
            scale=alt.Scale(domain=[0, upper]),
            axis=alt.Axis(
                grid=False,
                labels=False,
                ticks=False
            )
        ),
        tooltip=[
            alt.Tooltip("Name:N", title=label),
            alt.Tooltip("Display:N", title=value)
        ]
    )

    bars = base.mark_bar(
        color="#60966A",
        cornerRadiusEnd=7,
        size=24
    )

    labels = base.mark_text(
        align="left",
        dx=8,
        fontSize=12,
        color=DARK,
        fontWeight=600
    ).encode(
        text="Display:N"
    )

    chart = (bars + labels).properties(
        height=max(170, len(data) * 39)
    )

    st.altair_chart(
        chart_style(chart),
        use_container_width=True,
        theme=None
    )


def donut_chart(series):

    series = series[series > 0]

    if series.empty:
        st.info("No spending recorded yet.")
        return

    data = series.rename("Amount").reset_index()
    data.columns = ["Category", "Amount"]

    total = float(data["Amount"].sum())

    data["Share"] = (
        data["Amount"] / total
    )

    data["Spending"] = data["Amount"].map(money)

    donut = (
        alt.Chart(data)
        .mark_arc(
            innerRadius=65,
            outerRadius=100,
            cornerRadius=5
        )
        .encode(
            theta="Amount:Q",
            color=alt.Color(
                "Category:N",
                scale=alt.Scale(range=PALETTE),
                legend=alt.Legend(
                    title=None,
                    orient="bottom",
                    columns=2,
                    labelLimit=200
                )
            ),
            tooltip=[
                alt.Tooltip(
                    "Category:N",
                    title="Category"
                ),
                alt.Tooltip(
                    "Spending:N",
                    title="Spending"
                ),
                alt.Tooltip(
                    "Share:Q",
                    title="Share",
                    format=".1%"
                )
            ]
        )
    )

    center = (
        alt.Chart(pd.DataFrame({
            "Text": [money(total)]
        }))
        .mark_text(
            fontSize=25,
            fontWeight="bold",
            color=DARK
        )
        .encode(text="Text:N")
    )

    chart = (donut + center).properties(
        height=270
    )

    st.altair_chart(
        chart_style(chart),
        use_container_width=True,
        theme=None
    )


def trend_chart(series):

    if series.empty:
        st.info("No spending recorded yet.")
        return

    data = series.rename("Spending").reset_index()

    data.columns = ["Month", "Spending"]

    data["Date"] = pd.to_datetime(
        data["Month"],
        errors="coerce"
    )

    data = data.dropna(subset=["Date"])

    if data.empty:
        st.info("No dated spending records available.")
        return

    base = alt.Chart(data).encode(
        x=alt.X(
            "Date:T",
            title=None,
            axis=alt.Axis(
                format="%b %y",
                labelAngle=0,
                tickCount="month"
            )
        ),
        y=alt.Y(
            "Spending:Q",
            title="Spending (£)",
            scale=alt.Scale(zero=True)
        ),
        tooltip=[
            alt.Tooltip(
                "Date:T",
                title="Month",
                format="%B %Y"
            ),
            alt.Tooltip(
                "Spending:Q",
                title="Spending (£)",
                format=",.2f"
            )
        ]
    )

    area = base.mark_area(
        color="#83B692",
        opacity=0.22
    )

    line = base.mark_line(
        color=GREEN,
        strokeWidth=3
    )

    points = base.mark_point(
        color=GREEN,
        filled=True,
        size=65
    )

    chart = (area + line + points).properties(
        height=250
    )

    st.altair_chart(
        chart_style(chart),
        use_container_width=True,
        theme=None
    )


# ==========================================
# SESSION STATE
# ==========================================

defaults = {
    "submitted": set(),
    "claimed": {},
    "saved_offers": set(),
    "budgets": {},
    "page": "Home"
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ==========================================
# HEADER AND VIEW SELECTION
# ==========================================

st.markdown("# 🌿 Family Perks")
st.markdown("Little savings. Big family benefits.")

view = st.radio(
    "Choose your experience",
    ["Consumer view", "P&G insights"],
    horizontal=True
)

if view == "Consumer view":

    st.markdown("""
    <style>
    .block-container {
        max-width: 680px;
    }
    </style>
    """, unsafe_allow_html=True)


# ==========================================
# CONSUMER DASHBOARD
# ==========================================

if view == "Consumer view":

    with st.expander(
        "Choose a demo household",
        expanded=False
    ):

        consumer = st.selectbox(
            "Household profile",
            sorted(df["Consumer ID"].unique())
        )

        st.caption(
            "Synthetic consumer profiles for demonstration."
        )

    full_household = df[
        df["Consumer ID"] == consumer
    ].copy()

    all_receipts = (
        full_household
        .drop_duplicates("Receipt ID")
        .sort_values("Date")
    )

    reserve_count = min(
        10,
        max(0, len(all_receipts) - 1)
    )

    pending_ids = (
        set(all_receipts.tail(reserve_count)["Receipt ID"])
        if reserve_count > 0
        else set()
    )

    uploaded_ids = {
        receipt
        for owner, receipt in st.session_state.submitted
        if owner == consumer
    }

    household = full_household[
        (~full_household["Receipt ID"].isin(pending_ids))
        |
        full_household["Receipt ID"].isin(uploaded_ids)
    ].copy()

    receipts = household.drop_duplicates(
        "Receipt ID"
    ).copy()

    products = (
        household.groupby("Product Name")
        .agg(
            Trips=("Receipt ID", "nunique"),
            Spending=("Line Total", "sum"),
            Units=("Quantity", "sum")
        )
        .sort_values(
            ["Trips", "Spending"],
            ascending=False
        )
    )

    repeat_products = products[
        products["Trips"] >= 3
    ]

    uploaded = len(uploaded_ids)

    claimed = st.session_state.claimed.get(
        consumer, 0
    )

    available_rewards = max(
        0,
        uploaded // 10 - claimed
    )

    progress = (
        10 if available_rewards
        else uploaded % 10
    )

    offers = []

    for product, row in repeat_products.iterrows():

        for brand, discount in OFFER_VALUES.items():

            if brand in product.lower():

                offers.append({
                    "Product": product,
                    "Discount": discount,
                    "Trips": int(row["Trips"])
                })

                break

    potential_savings = sum(
        o["Discount"] for o in offers
    )

    # Navigation buttons

    pages = [
        ("Home", "🏠"),
        ("Scan", "📸"),
        ("Offers", "🏷️"),
        ("Budget", "📊"),
        ("Card", "💳")
    ]

    nav = st.columns(5)

    for col, (name, icon) in zip(nav, pages):

        if col.button(
            f"{icon} {name}",
            key=f"nav-{name}",
            use_container_width=True
        ):

            st.session_state.page = name

    page = st.session_state.page

    st.divider()


    # ======================================
    # HOME
    # ======================================

    if page == "Home":

        st.markdown("""
        <div class="hero">
            <span class="eyebrow">
                YOUR FAMILY. YOUR SAVINGS.
            </span>
            <h2>Welcome to Family Perks!</h2>
            <p>Make every shopping trip count.</p>
        </div>
        """, unsafe_allow_html=True)

        a, b = st.columns(2)

        a.metric(
            "Total recorded spending",
            money(receipts["Total Spend"].sum())
        )

        b.metric(
            "Available offer savings",
            money(potential_savings)
        )

        # Reward progress

        st.markdown(
            f"""
            <div class="reward">
                <h3>🎁 Your next family reward</h3>
                <div class="reward-number">
                    {progress}/10
                </div>
                <p>Shopping receipts submitted</p>
                <div class="track" style="height:16px;">
                    <div class="fill"
                         style="width:{progress * 10}%">
                    </div>
                </div>
                <p style="margin-top:15px;">
                    Unlock a £5 demo shopping voucher
                    for every 10 new receipts.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if available_rewards:

            st.success(
                "Congratulations! Your reward is ready."
            )

            if st.button(
                "🎁 Claim my £5 reward",
                use_container_width=True
            ):

                st.session_state.claimed[consumer] = (
                    claimed + 1
                )

                st.rerun()

        else:

            st.caption(
                f"Only {10-progress} more receipts to go!"
            )

        if st.button(
            "📸 Add a shopping receipt",
            use_container_width=True
        ):

            st.session_state.page = "Scan"
            st.rerun()

        # Budget summary

        st.subheader("Your monthly budget")

        dated = receipts.dropna(subset=["Date"])

        if not dated.empty:

            latest_month = (
                dated["Date"].max().to_period("M")
            )

            monthly = dated[
                dated["Date"].dt.to_period("M")
                == latest_month
            ]

            spent = monthly["Total Spend"].sum()

            budget = st.session_state.budgets.get(
                consumer, 500
            )

            st.markdown(
                f"""
                <div class="card">
                    <p>
                        {latest_month.strftime('%B %Y')}
                    </p>
                    <h2>{money(spent)}</h2>
                    <p>of your {money(budget)} budget</p>
                    <div class="track">
                        <div class="fill"
                            style="width:{
                                min(100, spent/budget*100)
                            }%">
                        </div>
                    </div>
                    <p style="margin-top:12px;">
                        {
                            money(budget-spent) + " remaining"
                            if spent <= budget
                            else money(spent-budget) + " over budget"
                        }
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Shopping favourites

        st.subheader("🛒 Your shopping favourites")

        if not products.empty:

            highest = max(1, products["Trips"].max())

            receipt_count = len(receipts)

            for product, row in products.head(5).iterrows():

                icon = ICONS.get(
                    category(product), "📦"
                )

                width = row["Trips"] / highest * 100

                st.markdown(
                    f"""
                    <div class="product-row">
                        <div class="product-header">
                            <div class="product-name">
                                {icon}
                                {html.escape(product.title())}
                            </div>
                            <div class="product-count">
                                {int(row['Trips'])} shops
                            </div>
                        </div>
                        <div class="track">
                            <div class="fill"
                                style="width:{width}%">
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.caption(
                f"Based on {receipt_count} recorded receipts."
            )

        # Offer notification

        st.subheader("💚 Picked for your family")

        if offers:

            st.success(
                f"You have {len(offers)} personalised "
                f"offers worth {money(potential_savings)}."
            )

            if st.button(
                "Explore my offers",
                use_container_width=True
            ):

                st.session_state.page = "Offers"
                st.rerun()

        else:

            st.info(
                "Keep adding receipts to unlock "
                "discounts on your regular purchases."
            )


    # ======================================
    # SCAN RECEIPT
    # ======================================

    elif page == "Scan":

        st.title("📸 Add a receipt")

        st.write(
            "Turn your everyday shopping into rewards."
        )

        st.progress(progress / 10)

        st.caption(
            f"{progress}/10 receipts towards your next reward"
        )

        available = full_household[
            full_household["Receipt ID"].isin(
                pending_ids - uploaded_ids
            )
        ].drop_duplicates("Receipt ID")

        if not available.empty:

            selected = st.selectbox(
                "Select a shopping receipt",
                available["Receipt ID"].tolist()
            )

            sample = full_household[
                full_household["Receipt ID"] == selected
            ]

            info = sample.iloc[0]

            store = html.escape(
                str(info["Store Name"])
            )

            date = (
                info["Date"].strftime("%d %B %Y")
                if pd.notna(info["Date"])
                else "Date unavailable"
            )

            rows = ""

            for _, item in sample.iterrows():

                product = html.escape(
                    str(item["Product Name"]).title()
                )

                quantity = int(item["Quantity"])

                price = money(item["Line Total"])

                rows += f"""
                <div class="receipt-row">
                    <span>
                        {product} × {quantity}
                    </span>
                    <strong>{price}</strong>
                </div>
                """

            st.subheader("Receipt preview")

            st.markdown(
                f"""
                <div class="receipt">
                    <h2>🧾 {store}</h2>
                    <p>{date}</p>
                    <p style="font-size:12px;">
                        Receipt:
                        {html.escape(str(selected))}
                    </p>
                    <hr>
                   {rows}<div class="receipt-total"><span>Total</span><span>{money(info['Total Spend'])}</span></div>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                "✓ Confirm and upload receipt",
                use_container_width=True
            ):

                st.session_state.submitted.add(
                    (consumer, selected)
                )

                st.toast(
                    "Receipt added to your family account!"
                )

                st.rerun()

        else:

            st.success(
                "All available demo receipts for "
                "this household have been uploaded."
            )

        st.caption(
            "Demo mode: receipts are drawn from "
            "the supplied synthetic database."
        )

        with st.expander("Upload a receipt photograph"):

            photograph = st.file_uploader(
                "Choose a receipt image",
                type=["jpg", "jpeg", "png"]
            )

            if photograph is not None:

                st.image(
                    photograph,
                    width=250
                )

                st.info(
                    "Image preview only. Automatic "
                    "receipt recognition is not yet enabled. "
                    "This does not count towards rewards."
                )

        st.subheader("Your recent shopping trips")

        recent = receipts.sort_values(
            "Date",
            ascending=False
        ).head(5)

        for _, receipt in recent.iterrows():

            store = html.escape(
                str(receipt["Store Name"])
            )

            date = (
                receipt["Date"].strftime("%d %b %Y")
                if pd.notna(receipt["Date"])
                else "Unknown date"
            )

            st.markdown(
                f"""
                <div class="product-row">
                    <div class="product-header">
                        <div>
                            <strong>🛒 {store}</strong>
                            <p>{date}</p>
                        </div>
                        <strong>
                            {money(receipt['Total Spend'])}
                        </strong>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


    # ======================================
    # PERSONALISED OFFERS
    # ======================================

    elif page == "Offers":

        st.title("🏷️ Your family offers")

        st.markdown(
            f"""
            <div class="hero">
                <span class="eyebrow">
                    PERSONALISED SAVINGS
                </span>
                <h1>{money(potential_savings)}</h1>
                <p>Potential savings on your favourites</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write(
            "Discounts inspired by products your "
            "household has bought at least three times."
        )

        for offer in offers:

            product = offer["Product"]

            discount = offer["Discount"]

            trips = offer["Trips"]

            icon = ICONS.get(
                category(product), "📦"
            )

            st.markdown(
                f"""
                <div class="card">
                    <p>💚 A household favourite</p>
                    <h3>
                        {icon}
                        {html.escape(product.title())}
                    </h3>
                    <div class="offer-badge">
                        {money(discount)} OFF
                    </div>
                    <p style="margin-top:12px;">
                        Bought on {trips}
                        separate shopping trips.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

            key = (consumer, product)

            if key in st.session_state.saved_offers:

                st.success("✓ Saved to your Family Perks card")

            elif st.button(
                "Save offer",
                key=f"offer-{consumer}-{product}",
                use_container_width=True
            ):

                st.session_state.saved_offers.add(key)

                st.rerun()

        if not offers:

            st.info(
                "You haven't unlocked any personalised "
                "offers yet. Keep scanning receipts!"
            )

        st.caption(
            "Offers are illustrative and are not "
            "redeemable retailer coupons."
        )


    # ======================================
    # FAMILY BUDGET
    # ======================================

    elif page == "Budget":

        st.title("📊 Your family budget")

        receipts["Month"] = (
            receipts["Date"]
            .dt.to_period("M")
            .astype(str)
        )

        household["Month"] = (
            household["Date"]
            .dt.to_period("M")
            .astype(str)
        )

        months = sorted(
            [
                m for m in receipts["Month"].unique()
                if m != "NaT"
            ],
            reverse=True
        )

        if not months:

            st.info("Upload a dated receipt to begin.")

        else:

            month = st.selectbox(
                "Shopping month",
                months
            )

            budget = st.number_input(
                "Monthly shopping budget (£)",
                min_value=50,
                max_value=10000,
                value=st.session_state.budgets.get(
                    consumer, 500
                ),
                step=25,
                key=f"budget-{consumer}"
            )

            st.session_state.budgets[consumer] = budget

            monthly_receipts = receipts[
                receipts["Month"] == month
            ]

            monthly_products = household[
                household["Month"] == month
            ]

            spent = monthly_receipts["Total Spend"].sum()

            remaining = budget - spent

            st.markdown(
                f"""
                <div class="hero">
                    <span class="eyebrow">
                        MONTHLY SHOPPING SPEND
                    </span>
                    <h1>{money(spent)}</h1>
                    <p>
                        Your monthly budget:
                        {money(budget)}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

            a, b = st.columns(2)

            a.metric(
                "Remaining" if remaining >= 0 else "Over budget",
                money(abs(remaining))
            )

            b.metric(
                "Shopping trips",
                len(monthly_receipts)
            )

            st.progress(
                max(0.0, min(1.0, spent / budget))
            )

            st.write(
                f"**{spent / budget * 100:.0f}% "
                f"of your budget used**"
            )

            if remaining < 0:

                st.warning(
                    f"You are {money(abs(remaining))} "
                    "over your monthly budget."
                )

            else:

                st.success(
                    f"You have {money(remaining)} "
                    "left this month."
                )

            st.subheader("Where your money goes")

            category_spending = (
                monthly_products
                .groupby("Category")["Line Total"]
                .sum()
                .sort_values(ascending=False)
            )

            donut_chart(category_spending)

            st.caption(
                "Product categories are estimated "
                "from receipt product names."
            )

            for name, value in category_spending.items():

                st.markdown(
                    f"""
                    <div class="product-row">
                        <div class="product-header">
                            <strong>
                                {ICONS.get(name, '📦')}
                                {html.escape(name)}
                            </strong>
                            <strong>{money(value)}</strong>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.subheader("Spending over time")

            trend_chart(
                receipts.groupby("Month")[
                    "Total Spend"
                ].sum()
            )

            st.subheader("Your favourite supermarkets")

            horizontal_chart(
                monthly_receipts.groupby(
                    "Store Name"
                )["Total Spend"].sum(),
                label="Supermarket",
                value="Total spending",
                currency=True
            )

            st.subheader("Your biggest expenses")

            horizontal_chart(
                monthly_products.groupby(
                    "Product Name"
                )["Line Total"].sum().nlargest(5),
                value="Total spending",
                currency=True
            )

            st.subheader("Most frequently purchased")

            horizontal_chart(
                products["Trips"].head(5),
                value="Shopping trips"
            )


    # ======================================
    # FAMILY PERKS WALLET CARD
    # ======================================

    elif page == "Card":

        st.title("💳 Your Family Perks card")

        member = hashlib.sha1(
            consumer.encode()
        ).hexdigest()[:8].upper()

        saved = sum(
            owner == consumer
            for owner, product
            in st.session_state.saved_offers
        )

        barcode = (
            "▏▌▏▎▌▍▏▌▎▍▌▏▌"
            "▍▏▌▎▌▏▍▌▏▎▍"
        )

        st.markdown(
            f"""
            <div class="wallet">
                <p>✳ FAMILY PERKS</p>
                <p style="font-size:12px;">
                    POWERED BY P&G
                </p>
                <h2>Family Savings Card</h2>
                <hr>
                <p>DEMO VOUCHERS EARNED</p>
                <h1>{money(claimed * 5)}</h1>
                <p>{saved} personalised offers saved</p>
                <p>{uploaded} new receipts submitted</p>
                <div class="wallet-code">
                    <div style="
                        font-size:32px;
                        overflow:hidden;
                        white-space:nowrap;
                    ">
                        {barcode}
                    </div>
                    <strong>FP-{member}</strong>
                </div>
                <p style="margin-top:15px;">
                    Scan at participating retailers
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.button(
            "Add to Apple Wallet",
            disabled=True,
            use_container_width=True
        )

        st.caption(
            "Visual Apple Wallet mock-up only. "
            "The barcode is decorative, not scannable."
        )

        st.subheader("Your rewards")

        st.metric(
            "Demo reward vouchers earned",
            money(claimed * 5)
        )

        st.metric(
            "Personalised offers saved",
            saved
        )


# ==========================================
# P&G BUSINESS DASHBOARD
# ==========================================

else:

    st.markdown("""
    <div class="hero">
        <span class="eyebrow">
            FAMILY PERKS | BUSINESS INTELLIGENCE
        </span>
        <h1>P&G Consumer Insights</h1>
        <p>
            Turning everyday shopping receipts into
            actionable consumer intelligence.
        </p>
    </div>
    """, unsafe_allow_html=True)

    panel = df.copy()

    panel_receipts = panel.drop_duplicates(
        ["Consumer ID", "Receipt ID"]
    ).copy()

    panel_receipts["Month"] = (
        panel_receipts["Date"]
        .dt.to_period("M")
        .astype(str)
    )

    st.subheader("Research panel overview")

    a, b, c, d = st.columns(4)

    a.metric(
        "Consumers",
        f"{panel['Consumer ID'].nunique():,}"
    )

    b.metric(
        "Shopping receipts",
        f"{len(panel_receipts):,}"
    )

    c.metric(
        "Purchase records",
        f"{len(panel):,}"
    )

    d.metric(
        "Retailers",
        panel["Store Name"].nunique()
    )

    a, b = st.columns(2)

    a.metric(
        "Total recorded expenditure",
        money(panel_receipts["Total Spend"].sum())
    )

    b.metric(
        "Average shopping basket",
        money(panel_receipts["Total Spend"].mean())
    )

    st.caption(
        "Aggregated historical synthetic receipt dataset."
    )

    st.divider()

    dashboard = st.radio(
        "Insights dashboard",
        [
            "Overview",
            "Brand loyalty",
            "Retailers",
            "Engagement"
        ],
        horizontal=True
    )


    # ======================================
    # BUSINESS OVERVIEW
    # ======================================

    if dashboard == "Overview":

        st.subheader("Most purchased products")

        popularity = (
            panel.drop_duplicates(
                [
                    "Consumer ID",
                    "Receipt ID",
                    "Product Name"
                ]
            )
            .groupby("Product Name")
            .size()
            .nlargest(10)
        )

        popularity.index = (
            popularity.index.str.title()
        )

        horizontal_chart(
            popularity,
            value="Receipt appearances"
        )

        st.subheader("Consumer spending over time")

        trend_chart(
            panel_receipts.groupby("Month")[
                "Total Spend"
            ].sum()
        )

        st.subheader("Category spending")

        categories = panel.groupby(
            "Category"
        )["Line Total"].sum()

        donut_chart(categories)

        st.caption(
            "Categories are estimated from product names."
        )


    # ======================================
    # BRAND LOYALTY
    # ======================================

    elif dashboard == "Brand loyalty":

        st.subheader("P&G repeat-purchase behaviour")

        brand_patterns = {
            "Fairy": ["fairy"],
            "Ariel": ["ariel"],
            "Lenor": ["lenor"],
            "Pantene": ["pantene"],
            "Oral-B": ["oral-b", "oral b"],
            "Head & Shoulders": [
                "head and shoulders",
                "head & shoulders"
            ],
            "Pampers": ["pampers"],
            "Gillette": ["gillette"]
        }

        loyalty = []

        for brand, patterns in brand_patterns.items():

            matches = pd.Series(
                False,
                index=panel.index
            )

            for pattern in patterns:

                matches = matches | (
                    panel["Product Name"].str.contains(
                        pattern,
                        case=False,
                        regex=False
                    )
                )

            brand_data = panel[matches]

            if not brand_data.empty:

                counts = brand_data.groupby(
                    "Consumer ID"
                )["Receipt ID"].nunique()

                buyers = len(counts)

                repeat_buyers = int(
                    (counts >= 3).sum()
                )

                loyalty.append({
                    "Brand": brand,
                    "Consumers": buyers,
                    "Repeat buyers": repeat_buyers,
                    "Repeat rate": round(
                        repeat_buyers / buyers * 100,
                        1
                    )
                })

        loyalty_df = pd.DataFrame(loyalty)

        if not loyalty_df.empty:

            horizontal_chart(
                loyalty_df.set_index("Brand")[
                    "Repeat rate"
                ],
                label="Brand",
                value="Repeat-purchase rate",
                percentage=True
            )

            st.caption(
                "Repeat rate: percentage of observed "
                "brand buyers purchasing the brand "
                "on at least three receipts."
            )

            st.subheader("Brand audience size")

            horizontal_chart(
                loyalty_df.set_index("Brand")[
                    "Consumers"
                ],
                label="Brand",
                value="Unique consumers"
            )

            st.dataframe(
                loyalty_df,
                hide_index=True,
                use_container_width=True
            )

        st.subheader("Potential coupon audiences")

        counts = (
            panel.groupby(
                ["Consumer ID", "Product Name"]
            )["Receipt ID"]
            .nunique()
            .reset_index(name="Trips")
        )

        audience = (
            counts[counts["Trips"] >= 3]
            .groupby("Product Name")["Consumer ID"]
            .nunique()
            .nlargest(10)
        )

        audience.index = audience.index.str.title()

        horizontal_chart(
            audience,
            value="Eligible consumers"
        )

        st.caption(
            "Consumers who purchased each product on "
            "at least three separate receipts. Includes "
            "P&G and non-P&G products."
        )


    # ======================================
    # RETAILER ANALYTICS
    # ======================================

    elif dashboard == "Retailers":

        st.subheader("Spending across supermarkets")

        horizontal_chart(
            panel_receipts.groupby(
                "Store Name"
            )["Total Spend"].sum(),
            label="Retailer",
            value="Total expenditure",
            currency=True
        )

        st.subheader("Retailer shopping frequency")

        horizontal_chart(
            panel_receipts.groupby(
                "Store Name"
            ).size(),
            label="Retailer",
            value="Shopping receipts"
        )

        st.subheader("Average basket size")

        horizontal_chart(
            panel_receipts.groupby(
                "Store Name"
            )["Total Spend"].mean(),
            label="Retailer",
            value="Average basket",
            currency=True
        )


    # ======================================
    # CONSUMER ENGAGEMENT
    # ======================================

    elif dashboard == "Engagement":

        st.subheader("Family Perks participation")

        submitted = st.session_state.submitted

        active_consumers = len({
            owner for owner, receipt in submitted
        })

        rewards_claimed = sum(
            st.session_state.claimed.values()
        )

        a, b = st.columns(2)

        a.metric(
            "New demo submissions",
            len(submitted)
        )

        b.metric(
            "Active demo consumers",
            active_consumers
        )

        a, b = st.columns(2)

        a.metric(
            "Rewards claimed",
            rewards_claimed
        )

        b.metric(
            "Offers saved",
            len(st.session_state.saved_offers)
        )

        st.subheader("Reward programme activity")

        st.markdown(
            f"""
            <div class="card">
                <p>Illustrative voucher value issued</p>
                <h2>{money(rewards_claimed * 5)}</h2>
                <p>One £5 reward per 10 new receipts.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.caption(
            "Participation figures reflect actions taken "
            "during the current demo session. Sample "
            "submissions are not added again to the "
            "historical research totals."
        )

    st.divider()

    st.subheader("Strategic opportunities")

    st.markdown("""
    <div class="card">
        <h3>🎯 Personalised promotions</h3>
        <p>
            Identify repeat purchasers and design
            targeted offers around household needs.
        </p>
    </div>

    <div class="card">
        <h3>🔁 Understanding brand loyalty</h3>
        <p>
            Compare repeat-purchase patterns across
            products and competing retailers.
        </p>
    </div>

    <div class="card">
        <h3>📈 Continuous consumer insights</h3>
        <p>
            Encourage consistent receipt contributions
            through budgeting tools and family rewards.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.caption(
        "Demonstration dashboard only. "
        "The database does not establish actual "
        "family demographics, and this view is "
        "not a secure employee portal."
    )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.markdown("""
<div style="
    text-align:center;
    color:#536D5B;
    font-size:12px;
    padding:15px;
">
    🌿 FAMILY PERKS 3.0<br>
    Powered by P&G · Hackathon Prototype<br>
    Synthetic data · Illustrative rewards
</div>
""", unsafe_allow_html=True)

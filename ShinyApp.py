import matplotlib
matplotlib.use("Agg")

from shiny import App, ui, render, reactive
# from shinywidgets import output_plotly, render_plotly
from plotnine import ggplot, aes, geom_bar, geom_line, geom_point, geom_text
from plotnine import theme_minimal, theme, labs, scale_x_continuous, scale_y_continuous, element_text
import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np
import os

def prepare_datasets():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "Datasets")
    sales_path = os.path.join(DATA_DIR, 'sales_data.csv')
    mall_path = os.path.join(DATA_DIR, 'shopping_mall_data.csv')

    mall = pd.read_csv(sales_path)

    mall['invoice_date'] = pd.to_datetime(mall['invoice date'])
    mall['Month'] = mall['invoice_date'].dt.month
    mall['Year'] = mall['invoice_date'].dt.year

    mall = mall.drop(["invoice date"], axis=1)
    mall = mall.sort_values("invoice_date")

    mall_details = pd.read_csv(mall_path)

    return mall, mall_details

mall_revenue_data, mall_details = prepare_datasets()
html_content = """
    <html>
        <h1><strong>California Mall Dataset</strong></h1><br>
        <h3>Author and Details</h3>
        <p>
            <strong>Author: </strong>Waken Cean C. Maclang <br>
            <strong>Course: </strong>BS Computer Science 3rd Year <br> 
            <strong>CSDS 312 - </strong> Machine Problem 3 <br>
            <br>
            Originally, the mini project was aimed to have multiple panels for revenue, category, customer details, and customer clustering.<br>
            However, due to time constraints, I've limited it first to supermarket sales on revenue and transactions based on product categories.<br>
        </p>
        <h3>All about the Dashboard</h3>
        <p>
            This dashboard follows the DATA framework.
            <ul>
                <li>Define Audience: For mall owners & data scientists.</li>
                <li>Analyze Data: There is a huge decrease in revenue after January 2023.</li>
                <li>Tell your story: The dashboard allows for the users to freely see different queries in the dataset by picking the year, month, malls, and the categories.</li>
                <li>Act on findings: Stakeholders can then prioritize on which product categories to advertise given based on quantity sold and revenue.</li>
            </ul>

            I've designed it to allow data scientists and stakeholders to explore the dataset themselves. <br>
            Not because I am lazy, but because it will better allow for exploration of patterns determined by experts in said field.
        </p>
        <h3>All about the dataset</h3>
        <p>
            The dataset was taken from: <a href=https://www.kaggle.com/datasets/captaindatasets/istanbul-mall>https://www.kaggle.com/datasets/captaindatasets/istanbul-mall</a><br>
            It is a dataset comprising of 3 xlsx files, [1] supermarket sales, [2] customer data, [3] supermarket details<br>
            It is designed to have a comprehensive understanding of the transactions made in a mall, customers who bought them, <br>
            and characteristics of the mall (e.g., construction year, number of stores, etc.) that may help determine the reason for those sales
        </p>
    </html>
"""

app_ui = ui.page_navbar(
    # Nav Bar 1: Prices
    ui.nav_panel(
        'Mall Details',
        ui.layout_column_wrap(
            ui.card(
                ui.card_header('Select a mall to view its details'),
                ui.input_select(
                    id='details_select_mall',
                    label='Select mall',
                    choices=[
                        'Beverly Center', 'Del Amo Fashion Center', 'Fashion Valley', 'Glendale Galleria', 'Irvine Spectrum',
                        'South Coast Plaza', 'Stanford Shopping Center', 'The Grove', 'Westfield Century City', 'Westfield Valley Fair'
                    ] ,
                    selected=['Beverly Center'],
                    multiple=False
                )
            ),
            ui.card(
                ui.card_header('Mall Details:'),
                ui.output_ui('get_mall_details')
            )
        ),
        ui.layout_columns(
            
        )
    ),

    ui.nav_panel(
        "Revenue",
        ui.card(
            ui.HTML('<p><strong>This section focuses on the revenue of malls across time</strong></p>'), 
            ui.layout_columns(
                ui.card(
                    ui.card_header("Year Picker"),
                    ui.input_select(
                        id="select_year",
                        label="Select year",
                        choices=["2021", "2022", "2023"],
                        selected="2023"
                    )
                ),
                ui.card(
                    ui.card_header('Mall Picker'),
                    ui.input_select(
                        id='revenue_select_mall',
                        label='Select mall',
                        choices=[
                            'All', 'Beverly Center', 'Del Amo Fashion Center', 'Fashion Valley', 'Glendale Galleria', 'Irvine Spectrum',
                            'South Coast Plaza', 'Stanford Shopping Center', 'The Grove', 'Westfield Century City', 'Westfield Valley Fair'
                        ] ,
                        selected=['All'],
                        multiple=False
                    )
                )
            )
        ),
        ui.layout_columns(
            ui.card(
                ui.card_header("Total Revenue"),
                ui.output_text("total_revenue")
            ),
            ui.card(
                ui.card_header("Average Monthly Revenue"),
                ui.output_text("avg_monthly_revenue")
            ),
            ui.card(
                ui.card_header("Highest Earning Month"),
                ui.output_text("max_monthly_revenue")
            ),
        ),
        ui.card(ui.output_plot('line_monthly_revenue')),
        ui.card(ui.output_plot('bar_mall_revenue'))
    ),

    # Nav Bar 2: Product Categories
    ui.nav_panel(
        "Transactions",
        ui.card(
            ui.HTML('<p><strong>View the different categories among malls here</strong></p>'), 
            ui.layout_columns(
                ui.card(
                    ui.card_header("Year Picker"),
                    ui.input_select(
                        id="category_select_year",
                        label="Select year",
                        choices=["2021", "2022", "2023"],
                        selected="2023"
                    )
                ),
                ui.card(
                    ui.card_header('Mall Picker'),
                    ui.input_select(
                        id='category_select_mall',
                        label='Select mall',
                        choices=[
                            'All', 'Beverly Center', 'Del Amo Fashion Center', 'Fashion Valley', 'Glendale Galleria', 'Irvine Spectrum',
                            'South Coast Plaza', 'Stanford Shopping Center', 'The Grove', 'Westfield Century City', 'Westfield Valley Fair'
                        ] ,
                        selected=['All'],
                        multiple=False
                    )
                )
            )
        ),
        ui.card(
            ui.layout_columns(
                ui.card(
                    ui.card_header("Total # of Transactions"),
                    ui.output_text("total_transactions")
                ),
                ui.card(
                    ui.card_header("Average # of Monthly Transactions"),
                    ui.output_text("avg_transactions")
                ),
                ui.card(
                    ui.card_header("Highest Monthly Transactions"),
                    ui.output_text("max_monthly_transactions")
                )
            )
        ),
        ui.card(
            ui.card(
                ui.card_header('Month Picker'),
                ui.input_select(
                    id='select_month',
                    label='Select Month',
                    choices=["January", "February", "March", "April", "May", "June",
                                "July", "August", "September", "October", "November", "December"],
                    selected='January'
                )
            ),
            ui.layout_columns(
                ui.card(ui.output_plot('one_month_categorical_sales')),
            )
        ),
        ui.card(ui.output_plot('monthly_categorical_sales')),
        ui.layout_columns(
            ui.card(ui.output_plot('monthly_mall_category_sales')),
            ui.card(
                ui.HTML('<p><strong>Play around with the data to change the plot on the left</strong></p>'),
                ui.input_select(
                    id='category_select_year_plot',
                    label='Select Year',
                    choices=['2021', '2022', '2023'],
                    selected=['2023'],
                    multiple=False
                ),
                ui.input_checkbox_group(
                    id='category_select_mall_plot',
                    label='Select the malls to view',
                    choices=['Beverly Center', 'Del Amo Fashion Center', 'Fashion Valley', 'Glendale Galleria', 'Irvine Spectrum',
                            'South Coast Plaza', 'Stanford Shopping Center', 'The Grove', 'Westfield Century City', 'Westfield Valley Fair'],
                    selected=['Beverly Center', 'Del Amo Fashion Center'],
                    inline=True
                ),
                ui.input_select(
                    id='category_select_category_plot',
                    label='Select category',
                    choices=['Clothing', 'Souvenir', 'Food & Beverage', 'Cosmetics', 'Toys',
                            'Shoes', 'Books', 'Technology'],
                    selected=['Clothing'],
                    multiple=False
                )
            )
        )
    ),

    ui.nav_panel('Dashboard Description', ui.HTML(html_content)),

    title='California Mall Dashboard'
)


# ---- 3. SERVER ----
def server(input, output, session):

    # Nav Bar 1: Revenue
    @reactive.Calc
    def filtered_year():
        """
        Returnes a queried version of our dataset based on the selected year
        """
        year = int(input.select_year())
        return mall_revenue_data[mall_revenue_data["Year"] == year]

    @reactive.Calc
    def filtered_mall():
        """
        A 2nd query added over the filtered_year() dataset, where we will
        return the dataset based on the selected mall
        """
        df = filtered_year()
        mall = input.revenue_select_mall()
        if mall == 'All':
            return df
        return df[df['shopping_mall'].isin([mall])]

    @reactive.Calc
    def filtered_mall_details():
        selected_mall = input.details_select_mall()
        df = mall_details
        return df[df['shopping_mall'] == selected_mall]

    @output
    @render.ui
    def get_mall_details():
        df = filtered_mall_details()
        df.columns = ['Shopping Mall', 'Construction Year', 'Area (sqm)', 'Location', 'Store Count']
        items = "".join(
            f"<strong>{col}:</strong> {df[col].iloc[0]}"
            f"<br>"
            for col in df.columns
        )

        return ui.HTML(f"<ul style='padding-left:0; list-style:none;'>{items}</ul>")

    @output
    @render.text
    def total_revenue():
        df = filtered_mall()
        total = df["price"].sum()
        return f"$ {total:,.2f}"

    @output
    @render.text
    def avg_monthly_revenue():
        df = filtered_mall()
        monthly = df.groupby("Month")["price"].sum()
        avg = monthly.mean()
        return f"$ {avg:,.2f}"

    @output
    @render.text
    def max_monthly_revenue():
        month_array = ["January", "February", "March", "April", "May", "June",
                       "July", "August", "September", "October", "November", "December"]
        df = filtered_mall()
        month, price = df.groupby('Month')[['price']].sum().reset_index().sort_values('price', ascending=True).iloc[-1, 0:]
        return f'{month_array[int(month) - 1]} : $ {price:,.2f}'
    
    @output
    @render.plot
    def line_monthly_revenue():
        df = filtered_mall()[['Month', 'price']].groupby('Month').sum().reset_index()
        df = df.sort_values('Month', ascending=True)
        year = int(input.select_year())
        plot = (
            ggplot(df)
            + aes(x='Month', y='price')
            + geom_line()
            + geom_point(color='black')
            + scale_x_continuous(
                breaks= [i + 1 for i in range(12)], 
                labels=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
            )
            + labs(
                title=f'Monthly Revenue ({year})',
                x='Month',
                y='Revenue'
            )
            + theme_minimal()
        )
        return plot.draw()

    @output
    @render.plot
    def bar_mall_revenue():
        df = filtered_year()
        df = df.groupby('shopping_mall')[['price']].sum().reset_index().sort_values('price')
        df['label'] = df['price'].apply(lambda x: f"$ {x:,.2f}")
        # df['shopping_mall'] = pd.Categorical(
        #     df['shopping_mall'], 
        #     categories=df['shopping_mall'][::-1], 
        #     ordered=True
        # )

        plot = (
            ggplot(data=df)
            + aes(x='shopping_mall', y='price')
            + geom_bar(stat='identity', color='black', fill='blue')
            + geom_text(
                aes(label='label'),
                va='top',
                position='identity',
                nudge_y = 0.11 * df['price'].max() 
            )
            + labs(
                title = f'Total revenue per mall ({input.select_year()})',
                x='Mall',
                y='Revenue'
            )
            + theme_minimal()
            + theme(axis_text_x=element_text(rotation=45, ha='right'))
        )

        return plot.draw()

    # Nav Bar 2: Product Categories
    @reactive.Calc
    def category_filtered_year():
        """
        For the Product Categories Nav Bar.
        Returnes a queried version of our dataset based on the selected year
        """
        year = int(input.category_select_year())
        return mall_revenue_data[mall_revenue_data["Year"] == year]
    
    @reactive.Calc
    def category_filtered_mall():
        """
        For the Product Categories Nav Bar
        A 2nd query added over the filtered_year() dataset, where we will
        return the dataset based on the selected mall
        """
        df = category_filtered_year()
        mall = input.category_select_mall()
        if mall == 'All':
            return df
        return df[df['shopping_mall'].isin([mall])]
    
    @reactive.Calc
    def category_filtered_category_plot():
        """
        Returns a dataframe with the selected malls
        This is for the "Number of {category} sales per mall"
        """
        selected_malls = input.category_select_mall_plot()
        selected_category = input.category_select_category_plot()
        df = category_filtered_year()
        return df[np.logical_and(df['shopping_mall'].isin(selected_malls), df['category'].isin([selected_category]))]

    @reactive.Calc
    def category_filtered_month_plot():
        """
        A method used to filter for the selected month input.select_month()
        Used in the Category Pie Chart
        """
        month = input.select_month()
        month = 1 if month == 'January' else 2 if month == 'February' else 3 if month == 'March' else 4 if month == 'April' else 5 \
            if month == 'May' else 6 if month == 'June' else 7 if month == 'July' else 8 if month == 'August' else 9 if month == 'September' \
            else 10 if month  == 'October' else 11 if month  == 'November' else 12
        df = category_filtered_mall()
        df = df[df['Month'] == month]
        return df

    @output
    @render.text
    def total_transactions():
        df = category_filtered_mall()
        return df['invoice_no'].count()
    
    @output
    @render.text
    def avg_transactions():
        df = category_filtered_mall()
        return f'{df.groupby("Month")["invoice_no"].count().mean():,.0f}'
    
    @output
    @render.text
    def max_monthly_transactions():
        month_array = ["January", "February", "March", "April", "May", "June",
                       "July", "August", "September", "October", "November", "December"]
        df = category_filtered_mall()
        month, count = df.groupby('Month')['invoice_no'].count().reset_index().sort_values('invoice_no').iloc[-1, :]
        return f'{month_array[int(month) - 1]}: {count}'
    
    @output
    @render.plot
    def one_month_categorical_sales():
        df = category_filtered_month_plot()
        df = df.groupby(['Month', 'category'])['invoice_no'].count().reset_index()

        fig, ax = plt.subplots()
        ax.pie(df['invoice_no'], labels=df['category'], autopct='%1.1f%%')
        ax.set_title('Number of transactions per month')
        return fig

    @output
    @render.plot
    def monthly_categorical_sales():
        df = category_filtered_mall()
        df = df.groupby(['Month', 'category'])['invoice_no'].count().reset_index()
        title_1 = 'Transactions in the' if input.category_select_mall() != 'All' else 'Transactions in'
        title_2 = 'Mall' if input.category_select_mall() != 'All' else 'Malls'
        plot = (
            ggplot(data=df)
            + aes(x='Month', y='invoice_no', color='category')
            + geom_line()
            + geom_point()
            + labs(
                title=f'{title_1} {input.category_select_mall()} {title_2}',
                x='Month',
                y='Number of Transactions',
                color='Category'
            )
            + scale_x_continuous(
                breaks= [i + 1 for i in range(12)], 
                labels=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
            )
        )
        return plot.draw()
    
    @output
    @render.plot
    def monthly_mall_category_sales():
        chosen_category = input.category_select_category_plot()
        if not chosen_category:
            return (ggplot() + labs(title="Select a specific category.")).draw()
        
        df = category_filtered_category_plot()
        df = df.groupby(['Month', 'shopping_mall'])['invoice_no'].count().reset_index()
        plot = (
            ggplot(data=df)
            + aes(x='Month', y='invoice_no', color='shopping_mall')
            + geom_line()
            + geom_point()
            + labs(
                title=f'Number of {chosen_category} sales per mall',
                x='Month',
                y='Number of Transactions',
                color='Malls'
            )
            + scale_x_continuous(
                breaks= [i + 1 for i in range(12)], 
                labels=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
            )
        )
        return plot.draw()


app = App(app_ui, server)
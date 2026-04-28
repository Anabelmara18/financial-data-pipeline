with base as (
    select
        date,
        ticker,
        close
    from {{ ref('stg_stock_price') }}
),

returns as (
    select
        date,
        ticker,
        close,

        -- gets the previous day's close price for the same ticker
        lag(close) over (
            partition by ticker  -- separate calculation per ticker
            order by date        -- ordered by date
        ) as prev_close,

        -- calculates % change from previous day
        round(
            (
                (close - lag(close) over (partition by ticker order by date))
                / lag(close) over (partition by ticker order by date)
            )::numeric * 100
        , 2) as daily_return_pct

    from base
)

select * from returns
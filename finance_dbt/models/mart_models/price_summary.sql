with base as (
    select
        ticker,
        date,
        open,
        high,
        low,
        close,
        volume
    from {{ ref('stg_stock_price') }}
),

summary as (
    select
        ticker,
        round(min(low)::numeric, 2) as all_time_low,
        round(max(high)::numeric, 2) as all_time_high,
        round(avg(close)::numeric, 2) as avg_close,
        round(avg(volume)::numeric, 2) as avg_volume,
        round(max(close)::numeric, 2) as latest_close,
        count(*) as total_days

    from base
    group by ticker  -- ← only ticker, not date or close
)

select * from summary
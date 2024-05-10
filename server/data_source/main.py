import asyncio
import data_aggregation
import data_normalization

if __name__ == "__main__":
    asyncio.run(data_aggregation.main())
    data_normalization.main()

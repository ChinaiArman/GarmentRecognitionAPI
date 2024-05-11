"""
Author: ``@cc-dev-65535``
Version: ``1.0.0``

Description:
This module runs the data aggregation and data normalization processes.

Requirements:
This module requires the data_aggregation module in the same package.
This module requires the data_normalization module in the same package.

Usage:
To use this module from the command line, you can run the following command:
    ``python main.py``
This will execute the data aggregation and data normalization processes.
"""


import asyncio
import data_aggregation
import data_normalization


if __name__ == "__main__":
    asyncio.run(data_aggregation.main())
    data_normalization.main()

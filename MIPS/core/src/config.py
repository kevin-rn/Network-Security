class Config:

    def __init__(self, time_window: int = 5, block_time: int = 30, threshold: int = 3) -> None:
        """
        Config class;
        Within the time_window if an ip exceeds the threshold, it should be blocked for the duration of block_time
        """
        self.time_window = time_window
        self.block_time = block_time
        self.threshold = threshold

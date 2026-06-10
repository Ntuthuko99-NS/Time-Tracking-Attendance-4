class StatsCard:
    def __init__(
        self,
        title,
        value,
        subtitle=None,
        icon=None,
        trend=None,
        trend_up=True,
        icon_bg="blue",
        icon_color="blue",
    ):
        self.title = title
        self.value = value
        self.subtitle = subtitle
        self.icon = icon
        self.trend = trend
        self.trend_up = trend_up
        self.icon_bg = icon_bg
        self.icon_color = icon_color

    def display(self):
        print("=" * 40)

        if self.icon:
            print(f"Icon: {self.icon}")

        print(f"Title: {self.title}")
        print(f"Value: {self.value}")

        if self.subtitle:
            print(f"Subtitle: {self.subtitle}")

        if self.trend:
            trend_symbol = "▲" if self.trend_up else "▼"
            print(f"Trend: {trend_symbol} {self.trend}")

        print("=" * 40)


# Example Usage
active_card = StatsCard(
    title="Active Now",
    value=15,
    subtitle="of 25 employees",
    icon="👥"
)

hours_card = StatsCard(
    title="Hours Today",
    value="124.5",
    subtitle="worked",
    icon="⏰"
)

weekly_card = StatsCard(
    title="Weekly Hours",
    value="642.3",
    subtitle="this week",
    icon="📅",
    trend="+12%",
    trend_up=True
)

active_card.display()
hours_card.display()
weekly_card.display()

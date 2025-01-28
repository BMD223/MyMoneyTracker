import WidgetKit
import SwiftUI

struct Provider: AppIntentTimelineProvider {
    func placeholder(in context: Context) -> SimpleEntry {
        SimpleEntry(date: Date(), originalValue: 0, currentValue: 0, configuration: ConfigurationAppIntent())
    }

    func snapshot(for configuration: ConfigurationAppIntent, in context: Context) async -> SimpleEntry {
        SimpleEntry(date: Date(), originalValue: 0, currentValue: 0, configuration: configuration)
    }

    func timeline(for configuration: ConfigurationAppIntent, in context: Context) async -> Timeline<SimpleEntry> {
        var entries: [SimpleEntry] = []

        let (originalValue, currentValue) = await fetchData()

        let currentDate = Date()
        let entry = SimpleEntry(date: currentDate, originalValue: originalValue, currentValue: currentValue, configuration: configuration)
        entries.append(entry)

        // policy set to refresh after a certain time
        return Timeline(entries: entries, policy: .after(Date().addingTimeInterval(15))) // Refresh every 15 seconds
    }

    private func fetchData() async -> (Double, Double) {
        guard let url = URL(string: "http://127.0.0.1:6767/update") else { return (0, 0) }

        do {
            let (data, _) = try await URLSession.shared.data(from: url)
            if let json = try? JSONSerialization.jsonObject(with: data, options: []) as? [String: Any],
               let originalValue = json["original_value"] as? Double,
               let currentValue = json["current_value"] as? Double {
                return (originalValue, currentValue)
            }
        } catch {
            print("Failed to fetch or parse data: \(error)")
        }

        return (0, 0) // Default fallback values
    }
}

struct SimpleEntry: TimelineEntry {
    let date: Date
    let originalValue: Double
    let currentValue: Double
    let configuration: ConfigurationAppIntent
}

struct SimpleWidgetEntryView: View {
    var entry: Provider.Entry

    var body: some View {
        VStack {
            Spacer()

            VStack {
                Text("Current Balance:")
                Text(String(entry.currentValue))
                    .font(.headline)
                    .foregroundColor(.green)

                Text("Original Balance:")
                Text(String(entry.originalValue))
                    .font(.subheadline)
                    .foregroundColor(.blue)
            }
            .frame(maxWidth: .infinity, maxHeight: .infinity)
            .multilineTextAlignment(.center)

            Spacer()
        }
    }
}

extension NumberFormatter {
    static var decimalFormatter: NumberFormatter {
        let formatter = NumberFormatter()
        formatter.numberStyle = .decimal
        formatter.minimumFractionDigits = 0
        formatter.maximumFractionDigits = 2
        return formatter
    }
}

struct SimpleWidget: Widget {
    let kind: String = "SimpleWidget"

    var body: some WidgetConfiguration {
        AppIntentConfiguration(kind: kind, intent: ConfigurationAppIntent.self, provider: Provider()) { entry in
            SimpleWidgetEntryView(entry: entry)
                .containerBackground(.fill.tertiary, for: .widget)
        }
    }
}

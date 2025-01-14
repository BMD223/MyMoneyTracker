//
//  AppIntent.swift
//  SimpleWidget
//
//  Created by Bartosz Dziuba on 1/10/25.
//

import WidgetKit
import AppIntents

struct ConfigurationAppIntent: WidgetConfigurationIntent {
    
    static var title: LocalizedStringResource = "Configuration"
    static var description = IntentDescription("This is an example widget.")

    // An example configurable parameter.
    @Parameter(title: "Input Balance", default: 0)
    var inputBalance: Double
    
    @Parameter(title: "Current Balance", default: 0)
    var currentBalance: Double

    @Parameter(title: "Abs path", default: "../input.csv")
    var path: String
}

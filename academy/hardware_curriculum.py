def _quiz_question(prompt, correct_option, wrong_options, explanation):
    options = list(wrong_options)
    correct_index = sum(map(ord, prompt)) % (len(options) + 1)
    options.insert(correct_index, correct_option)
    return {
        "question": prompt,
        "options": options,
        "correct_index": correct_index,
        "explanation": explanation,
    }


BEGINNER_HARDWARE_TOPICS = [
    (
        "Motherboard: The Main Circuit Board",
        "The motherboard connects the CPU, memory, storage, and expansion devices. It sits inside the case, and its layout determines which components can be installed. A system that will not start may have a loose power connection, but diagnosis should begin with safe external checks.",
        "The computer has no power lights. What is the safest first check before considering internal connections?",
        ["Check the wall outlet and external power cable", "Remove the CPU while the computer is plugged in", "Open the power supply unit"],
        "Check the wall outlet and external power cable",
    ),
    (
        "HDD: Magnetic Long-Term Storage",
        "A hard disk drive stores files on spinning magnetic disks and usually connects to the motherboard with a data cable and to the power supply. Clicking sounds, slow reads, or missing files can indicate a drive problem. Back up important files and check drive health before replacing hardware.",
        "A workstation drive makes repeated clicking sounds and contains important files. What is the best first response?",
        ["Protect the data and follow the approved backup and drive-health process", "Keep restarting it until the noise stops", "Open the drive casing to inspect the disks"],
        "Protect the data and follow the approved backup and drive-health process",
    ),
    (
        "SSD: Fast Solid-State Storage",
        "A solid-state drive stores data in flash memory and has no spinning disks. It may be a 2.5-inch SATA drive or a small M.2 module on the motherboard. SSDs can make a computer start and load applications faster, but they still need backups and safe handling.",
        "Before replacing an SSD, what should a technician verify?",
        ["The correct drive type, size, interface, and backup plan", "That the replacement is a graphics card", "That the computer is still powered on"],
        "The correct drive type, size, interface, and backup plan",
    ),
    (
        "PSU: Power Supply Safety",
        "The power supply unit converts wall power into power used by computer components. It is usually mounted at the back of a desktop case. A faulty PSU can cause shutdowns or no power, but a beginner should never open the PSU because dangerous electrical energy may remain inside.",
        "A desktop PSU is suspected to be faulty. What is the safe action?",
        ["Disconnect the computer and refer PSU replacement to trained personnel; never open the PSU", "Open the PSU and touch its capacitors", "Test its internal parts while connected to mains power"],
        "Disconnect the computer and refer PSU replacement to trained personnel; never open the PSU",
    ),
    (
        "GPU: Graphics Processing Unit",
        "A graphics processing unit renders images and video. A desktop GPU may be an expansion card installed in a PCI Express slot; some computers use graphics built into the CPU. Display problems can also come from the monitor, cable, or selected input, so check those before replacing the GPU.",
        "A monitor shows no picture. What should you check before assuming the GPU has failed?",
        ["Monitor power, selected input, and display cable connections", "Delete the user's documents", "Open the power supply"],
        "Monitor power, selected input, and display cable connections",
    ),
    (
        "Cooling Fans and Airflow",
        "Fans move air through the case and across heat-producing parts such as the CPU and GPU. Dust, blocked vents, or a failed fan can cause high temperatures and unexpected shutdowns. Power down and unplug before external cleaning; never put fingers or tools into a moving fan.",
        "A desktop fan is noisy and the case vents are dusty. What should you do before cleaning?",
        ["Shut down, disconnect power, and follow the manufacturer's cleaning guidance", "Spray liquid cleaner into the running case", "Hold the spinning fan still with a finger"],
        "Shut down, disconnect power, and follow the manufacturer's cleaning guidance",
    ),
    (
        "BIOS and UEFI Firmware",
        "BIOS or UEFI firmware initializes hardware and helps start the operating system. Setup options are available before the operating system loads. Changing boot or security settings can prevent startup, so record the current setting and follow the device or organization guidance.",
        "A computer needs to boot from its internal drive. Where would you check the configured boot order?",
        ["BIOS or UEFI setup", "The printer queue", "The desktop wallpaper settings"],
        "BIOS or UEFI setup",
    ),
    (
        "Network Interface Card",
        "A network interface card (NIC) connects a computer to a wired or wireless network. It may be built into the motherboard or installed as an expansion card. If network access fails, check link status, airplane mode, and the cable or Wi-Fi connection before replacing the NIC.",
        "A wired desktop cannot reach the network. What should you inspect before replacing its NIC?",
        ["Ethernet link lights, cable seating, and network adapter status", "The CPU brand label", "The printer's paper tray"],
        "Ethernet link lights, cable seating, and network adapter status",
    ),
    (
        "Ethernet Cables and Connectors",
        "Ethernet cables connect devices to a router, switch, or wall port. The connector is commonly called RJ45. A damaged cable or loose connector can break a connection; inspect it for damage and try a known-good cable if policy allows.",
        "A computer reports that its wired connection is disconnected. What is a useful first cable check?",
        ["Confirm both ends are seated and inspect the cable for visible damage", "Pull the cable by its wires", "Change the computer's BIOS password"],
        "Confirm both ends are seated and inspect the cable for visible damage",
    ),
    (
        "Computer Ports and Connectors",
        "Ports connect peripherals and cables. USB, HDMI, DisplayPort, Ethernet, and audio connectors have different shapes and purposes. Forcing a connector can damage the port; identify the correct port and align the connector before inserting it.",
        "A USB connector does not fit easily into a port. What should you do?",
        ["Stop, check the connector orientation and port type, and never force it", "Push harder until it fits", "Use a metal tool to widen the port"],
        "Stop, check the connector orientation and port type, and never force it",
    ),
    (
        "Peripherals: Keyboard, Mouse, and Monitor",
        "Peripherals are devices connected to a computer, such as keyboards, mice, monitors, webcams, and headsets. When one stops working, check its power, connection, selected input, and settings before replacing it.",
        "A monitor is blank, but the computer appears to be running. What should you check first?",
        ["Monitor power, input selection, and video cable", "Reinstall the operating system immediately", "Replace the keyboard"],
        "Monitor power, input selection, and video cable",
    ),
    (
        "Power and Data Cables Inside a PC",
        "Internal components may use separate data and power cables. A loose connection can make a drive or fan disappear, but opening the case requires shutdown, unplugging, ESD precautions, and following the service guide.",
        "A desktop drive is not detected after the computer was moved. What should happen before checking internal cables?",
        ["Shut down, unplug the computer, and follow the service guide with ESD precautions", "Check cables while the computer is powered", "Open the PSU"],
        "Shut down, unplug the computer, and follow the service guide with ESD precautions",
    ),
    (
        "Storage Upgrade Planning",
        "Storage upgrades require checking the interface, physical size, capacity, and compatibility. Plan how data will be backed up or migrated before changing a drive. Follow the device manufacturer's instructions and verify the replacement before closing the case.",
        "A laptop needs a new storage drive. What should you check before ordering one?",
        ["The supported form factor, interface, device guide, and data backup plan", "Only the laptop's screen size", "Whether the new drive is a USB keyboard"],
        "The supported form factor, interface, device guide, and data backup plan",
    ),
    (
        "RAM Capacity and Compatibility",
        "RAM modules must match the motherboard's supported memory type and configuration. More memory can help when applications run out of available RAM, but installing incompatible memory may prevent booting. Check device specifications before buying or installing.",
        "Before adding RAM, what information should you confirm?",
        ["Supported memory type, capacity limits, and slot configuration", "The printer's toner level", "The user's browser history"],
        "Supported memory type, capacity limits, and slot configuration",
    ),
    (
        "Expansion Slots and Add-in Cards",
        "Expansion slots let a desktop accept add-in cards such as graphics or network adapters. Card size, slot type, case clearance, and power requirements matter. Follow the service guide and do not force a card into a slot.",
        "A new add-in card does not align with the available slot. What should you do?",
        ["Stop and verify the card type, slot, and device compatibility", "Force it into the slot", "Remove the motherboard label"],
        "Stop and verify the card type, slot, and device compatibility",
    ),
    (
        "ESD and Safe Component Handling",
        "Electrostatic discharge can damage sensitive parts without a visible spark. Work in an ESD-safe area, follow device instructions, and hold components by their edges. Power down and unplug first; do not touch connector contacts unnecessarily.",
        "How should you handle a loose memory module?",
        ["Hold it by the edges and follow ESD precautions", "Touch the gold contacts", "Place it on carpet and rub it to remove dust"],
        "Hold it by the edges and follow ESD precautions",
    ),
    (
        "Recognize Common Hardware Symptoms",
        "Hardware symptoms overlap, so one symptom rarely proves a specific component has failed. No display may involve a monitor or cable; slowness may involve software, storage, or memory. Ask questions, check indicators, and gather evidence before replacing parts.",
        "A computer is slow. What is a good troubleshooting approach?",
        ["Ask when it began and check resource use and storage before identifying a cause", "Replace the CPU immediately", "Assume every slow computer has a faulty GPU"],
        "Ask when it began and check resource use and storage before identifying a cause",
    ),
    (
        "Safe Cleaning and Preventive Maintenance",
        "Preventive maintenance includes keeping vents clear, checking cables, installing approved updates, and maintaining backups. Shut down and disconnect power before cleaning. Do not use liquids inside a computer or open a power supply.",
        "What is the safe way to clean dust around a desktop's external vents?",
        ["Power down and unplug, then follow manufacturer cleaning instructions", "Pour cleaner into the vents", "Open and service the PSU"],
        "Power down and unplug, then follow manufacturer cleaning instructions",
    ),
]


INTERMEDIATE_HARDWARE_TOPICS = [
    (
        "Intermediate: Diagnose a No-POST Condition",
        "POST is the firmware's power-on self-test. A system that powers on but does not complete POST may report diagnostic LEDs, beep codes, or a display message. Record the exact indicator and consult the model's service documentation instead of guessing at a failed part.",
        "A desktop powers on but shows a repeating diagnostic LED. What is the best next step?",
        ["Record the LED pattern and check the manufacturer's diagnostic guide", "Replace every component at once", "Open the PSU while it is connected"],
        "Record the LED pattern and check the manufacturer's diagnostic guide",
    ),
    (
        "Intermediate: Investigate Memory Errors",
        "Memory errors can cause crashes, boot failures, or corrupted work. Record symptoms and recent changes, then use an approved memory diagnostic and follow the service guide before reseating or replacing modules.",
        "A system reports memory errors. What should you do before removing a module?",
        ["Record the errors and follow the approved diagnostic and service procedure", "Pull a module while the computer is on", "Assume the operating system is the cause"],
        "Record the errors and follow the approved diagnostic and service procedure",
    ),
    (
        "Intermediate: Review SSD Health Indicators",
        "Storage devices may report health attributes through SMART or vendor tools. A warning is a reason to protect data and plan replacement, not a guarantee of how long a drive will last. Maintain backups and use approved diagnostics.",
        "A storage health tool reports a critical warning. What should be prioritized?",
        ["Protect and back up data, then follow the approved replacement process", "Run repeated stress tests before backing up", "Ignore it if files still open"],
        "Protect and back up data, then follow the approved replacement process",
    ),
    (
        "Intermediate: Diagnose Thermal Throttling",
        "Thermal throttling reduces performance when a component becomes too hot. Check temperatures and fan behavior using an approved tool, and inspect airflow and dust safely. Do not remove a heatsink or apply thermal compound unless trained and following the service guide.",
        "A computer slows under load and temperature readings are unusually high. What is a sensible next check?",
        ["Review fan operation and airflow using approved diagnostics", "Open the PSU", "Disable all thermal protections"],
        "Review fan operation and airflow using approved diagnostics",
    ),
    (
        "Intermediate: Distinguish PSU Symptoms from Other Faults",
        "A failing PSU can cause intermittent shutdowns or no power, but similar symptoms can have other causes. Check external power, document when the issue occurs, and use approved tools or trained service procedures. Never open a PSU or probe it while connected to mains.",
        "A PC shuts down intermittently. What is a safe way to continue investigating possible power issues?",
        ["Check external power and logs, then escalate for approved PSU testing", "Open the PSU and inspect it while plugged in", "Replace the motherboard without evidence"],
        "Check external power and logs, then escalate for approved PSU testing",
    ),
    (
        "Intermediate: Use POST Beep and LED Codes",
        "Diagnostic beep and LED patterns vary by manufacturer and model. The same sound can mean different things on different hardware. Record the exact pattern, model, and recent changes, then use the matching service documentation.",
        "A computer gives a beep code at startup. How do you interpret it?",
        ["Match the exact pattern to the correct model's service documentation", "Use a generic code from any computer brand", "Ignore the pattern and replace RAM"],
        "Match the exact pattern to the correct model's service documentation",
    ),
    (
        "Intermediate: Isolate a Graphics Display Fault",
        "A display fault can originate from the monitor, cable, selected input, graphics adapter, or driver. Test one known-good connection at a time and note whether the issue appears before or after the operating system loads.",
        "A user reports intermittent display loss. What is a useful isolation step?",
        ["Test a known-good cable and display input, changing one item at a time", "Replace the GPU before checking the monitor", "Update unrelated printer software"],
        "Test a known-good cable and display input, changing one item at a time",
    ),
    (
        "Intermediate: Troubleshoot a Network Adapter",
        "A NIC problem can be driver-, configuration-, or hardware-related. Compare link indicators, adapter status, and network settings; if policy allows, test a known-good cable or port. Avoid changing several settings at once.",
        "An Ethernet adapter shows no link. What is a useful controlled test?",
        ["Try a known-good cable and port, then compare adapter link status", "Change DNS repeatedly without recording the original values", "Replace the monitor"],
        "Try a known-good cable and port, then compare adapter link status",
    ),
    (
        "Intermediate: Check Component Compatibility",
        "Compatibility depends on the system model, motherboard, firmware, physical space, interface, and power budget. Verify the manufacturer specifications and organization approval before ordering or installing a part.",
        "Before installing a high-power graphics card, what should you verify?",
        ["System slot, physical clearance, supported power connections, and approved PSU capacity", "Only whether the card color matches the case", "Whether a USB port is free"],
        "System slot, physical clearance, supported power connections, and approved PSU capacity",
    ),
    (
        "Intermediate: Plan a Safe Hardware Replacement",
        "A safe replacement plan includes authorization, model identification, data protection, the correct replacement part, ESD preparation, and a post-installation check. Record the original symptoms and results so the fix can be verified.",
        "What should a technician do before starting an authorized internal hardware replacement?",
        ["Confirm the model and part, protect data, shut down, disconnect power, and prepare ESD controls", "Leave the system running to save time", "Discard the original diagnostic notes"],
        "Confirm the model and part, protect data, shut down, disconnect power, and prepare ESD controls",
    ),
]


def _build_lesson(path_slug, topic, order, difficulty):
    title, explanation, prompt, choices, answer = topic
    title_text = title.split(": ", 1)[-1]
    return {
        "path": path_slug,
        "title": title,
        "slug": f"hardware-topic-{order:02}",
        "short_description": explanation.split(". ", 1)[0] + ".",
        "introduction": (
            f"This {difficulty.lower()} lesson focuses on {title_text.lower()}. "
            "Learn what the component or procedure does, common symptoms, and how to "
            "investigate safely before changing hardware."
        ),
        "explanation": explanation,
        "activity_type": "concept",
        "activity_prompt": prompt,
        "activity_choices": choices,
        "starter_code": "",
        "expected_keywords": [],
        "hint": "Start with the safest external check, gather evidence, and follow the device service guide.",
        "answer": answer,
        "solution": (
            f"The best answer is: {answer}. {explanation} "
            "Never open a power supply, work on powered internal components, or force a connector. "
            "Follow manufacturer instructions and refer work to trained personnel when needed."
        ),
        "difficulty": difficulty,
        "order": order,
        "quiz": [
            _quiz_question(
                f"What is the key idea in {title_text.lower()}?",
                explanation,
                [
                    "Replace parts immediately without checking symptoms.",
                    "Ignore manufacturer safety guidance.",
                ],
                explanation,
            ),
            _quiz_question(
                f"What is a safe next step for this {title_text.lower()} activity?",
                answer,
                [
                    "Force a component or connector that does not fit.",
                    "Open a power supply to inspect internal parts.",
                ],
                f"{answer}. Follow the model-specific service guidance and gather evidence before changing hardware.",
            ),
            _quiz_question(
                "When should internal component work stop?",
                "When the device is powered, instructions are unclear, or the task is outside your training",
                [
                    "Only after a component has been damaged.",
                    "Never; all internal work is safe for beginners.",
                ],
                "Power down and disconnect before authorized internal work; stop and escalate if unsure or untrained.",
            ),
        ],
    }


def build_hardware_lessons():
    for order, topic in enumerate(BEGINNER_HARDWARE_TOPICS, start=3):
        yield _build_lesson("computer-hardware", topic, order, "Beginner")

    for order, topic in enumerate(INTERMEDIATE_HARDWARE_TOPICS, start=21):
        yield _build_lesson("computer-hardware", topic, order, "Intermediate")

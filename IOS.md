# Rotation on iPhone (Capacitor)

Needs on the Mac: Xcode (Mac App Store) and Node 22+ (`brew install node`).

    git clone https://github.com/tonedibias3/rotation && cd rotation
    npm install
    npm run sync        # copies the site into the iOS app
    npx cap open ios    # opens Xcode

In Xcode: click the blue "App" project > Signing & Capabilities > Team: pick your Apple ID.
Plug in the iPhone, choose it at the top, press Play. After any change to app/index.html, run `npm run sync` again.

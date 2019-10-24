from folker.load.files import load_test_files

tests = load_test_files()
for test in tests:
    test.execute()

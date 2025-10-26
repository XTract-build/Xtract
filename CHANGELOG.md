# Changelog

## [v0.25] - 2025-01-26 - Milestone 1 Complete ✅

### 🎉 Major Features Added
- **Function Body Generation**: Complete statement-level transpilation
  - `require(condition, "msg")` → `require!(condition, "msg")`
  - `emit EventName(args)` → `self.event_name_event(args)`
  - `return expression` → `return expression`
  - Variable assignments → Storage mapper operations
- **Error Handling**: Solidity `revert()` → MultiversX `sc_panic!()`
- **Nested Mapping Support**: `allowance[from][to]` → `self.allowance(&from, &to)`
- **Enhanced Type System**: Extended mappings for integers and better type conversions

### 🧪 Testing & Quality
- **100% Test Coverage**: All 5 test contracts pass comprehensive validation
- **Body-Level Assertions**: Tests now validate actual function implementations
- **CI/CD Pipeline**: GitHub Actions for automated testing
- **Demo Integration**: Working MultiversX-compatible demo crate

### 📚 Documentation
- **Early Adopter Guide**: Complete migration guidance and best practices
- **Updated README**: Clear feature status and limitations
- **Developer Guide**: Enhanced with current capabilities and limitations

### 🔧 Technical Improvements
- **Parser Enhancement**: Multi-level regex parsing for complex patterns
- **Expression Conversion**: Smart variable resolution and storage access
- **Storage Mapping**: Proper handling of nested mappings and arrays

### 📊 KPIs Achieved
- ✅ ≥90% unit test success rate (100% achieved)
- ✅ Public GitHub repository with CI
- ✅ Documentation published and comprehensive
- ✅ 5+ Solidity contracts successfully transpiled with body generation

### 🔄 Migration Notes for Users
- **Breaking Changes**: None - fully backward compatible
- **New Capabilities**: Function bodies now include implementation logic
- **SpaceVM Compatibility**: Enhanced support for MultiversX push model
- **Error Handling**: Improved conversion of Solidity error patterns

## [v0.2] - 2024-12-XX

Initial release with basic transpilation framework.

---

*For detailed implementation notes, see [transpiler_report.md](transpiler_report.md)*
